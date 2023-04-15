import logging
import time

import geopandas as gpd
import pandas as pd
import shapely
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)

def get_connection_url(settings) -> str:
    return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


def wait_for_db(engine: Engine, timeout: int = 60) -> None:
    """
    Wait until the database connection is available.

    Args:
        engine: A SQLAlchemy database engine.

    Raises:
        OperationalError: If the database connection cannot be established.

    """
    start_time = time.time()
    while True:
        try:
            engine.connect()
            break
        except OperationalError:
            print("Database not ready yet. Waiting...")
            time.sleep(5)
            if time.time() - start_time > timeout:
                raise TimeoutError("Timed out waiting for database to become available")


def should_create_table(engine: Engine, table: str) -> bool:
    """Check if a table exists in the database.

    Args:
        engine: A SQLAlchemy database engine.
        table (str): Name of the table to check.

    Returns:
        bool: True if the table does not exist in the database, False otherwise.
    """
    inspector = inspect(engine)
    return not inspector.has_table(table)


def write_data_to_db(
    engine: Engine, csv_file: str, raw_table_name: str, heatmap_table_name: str
) -> None:
    """Preprocess and write data to the database from the specified CSV file

    Convert csv file to geopandas DataFrame and write raw data to database.
    Calculate values for heatmap and write raw data to database.

    This serves as a simple example of saving data to database. The actual
    interaction should be given more thought: should app check the existence
    of data on every start up? Should duplicates be handled?

    """

    if not any(
        (
            should_create_table(engine, raw_table_name),
            should_create_table(engine, heatmap_table_name),
        )
    ):
        logger.warn("The data already exists")
        return

    df = pd.read_csv(csv_file)
    raw_geom_column = "footprints_used"
    geom_column = "geom"
    try:
        df[geom_column] = df[raw_geom_column].apply(shapely.from_geojson)
    except KeyError:
        raise KeyError(
            f"Excepted to read geometry from missing  `{raw_geom_column}` column"
        )

    df = df.drop(raw_geom_column, axis=1)
    gdf = gpd.GeoDataFrame(df)
    gdf = gdf.set_geometry(geom_column)
    # FIXME this is an assumtion
    gdf = gdf.set_crs("EPSG:4326")

    gdf.to_postgis(raw_table_name, con=engine)
    logger.info("Raw data is sucessfully written to db.")

    gdf["area"] = gdf.to_crs("+proj=cea").area
    gdf["geom"] = gdf.to_crs("+proj=cea").centroid.to_crs(gdf.crs)

    gdf.to_postgis(heatmap_table_name, con=engine)
    logger.info("Preprocessed data is sucessfully written to db.")


def get_org_ids_from_db(settings) -> list:
    engine = create_engine(get_connection_url(settings))
    conn = engine.connect()
    command = text(f"SELECT DISTINCT org_id FROM {settings.heatmap_table_name};")
    result = conn.execute(command)
    # use all to close the connection
    return [row[0] for row in result.all()]
