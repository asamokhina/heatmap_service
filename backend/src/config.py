from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DATA_SOURCE: str = ""
    FE_HOST: str = ""
    raw_table_name = "raw_polygons"
    heatmap_table_name = "heatmap_points"


settings = Settings()
