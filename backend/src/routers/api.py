import ast
import logging
from typing import List, Optional, TypeVar

import geopandas as gpd
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text

from src.config import settings
from src.utils import get_connection_url, get_org_ids_from_db

logger = logging.getLogger(__name__)

CoordType = TypeVar("CoordType", float, None)

router = APIRouter(prefix="/api")


@router.get("/org-ids", response_model=List[int])
async def get_org_ids() -> list[int]:
    "Get a list of unique org_ids from the database"
    return get_org_ids_from_db(settings)


@router.get("/data/{org_id}")
async def get_geodata(
    org_id: str,
    # minlat: Optional[CoordType] = None,
    # maxlat: Optional[CoordType] = None,
    # minlon: Optional[CoordType] = None,
    # maxlon: Optional[CoordType] = None,
):
    """Get data from the database within the given bounding box.

    Args:
        org_id: Organization id OR `Select All`
        # minlat: The minimum latitude of the bounding box.
        # maxlat: The maximum latitude of the bounding box.
        # minlon: The minimum longitude of the bounding box.
        # maxlon: The maximum longitude of the bounding box.

    Returns:
        A dictionary representation of the GeoDataFrame.
    """

    sql = f"""
            SELECT *
            FROM {settings.heatmap_table_name}
        """
    try:
        parsed_org_id = int(org_id)
        sql += f"""
            WHERE org_id = {parsed_org_id}
        """
    except ValueError:
        if org_id != "Select All":
            raise HTTPException(
                status_code=400, detail=(f"Invalid organizaition ID: {org_id}")
            )

    # if all((minlat, maxlat, minlon, maxlon)):
    #
    #     sql += f"""
    #         ST_Intersects(geom, ST_MakeEnvelope({minlon}, {minlat}, {maxlon}, {maxlat}, 4326))
    #     """

    engine = create_engine(get_connection_url(settings))
    fgdf = gpd.read_postgis(sql, engine)
    if fgdf.empty:
        raise HTTPException(
            status_code=404, detail=(f"No data for organizaition ID {org_id}")
        )
    # FIXME should be a nicer way
    result = ast.literal_eval(fgdf["geom"].to_json())
    return result
