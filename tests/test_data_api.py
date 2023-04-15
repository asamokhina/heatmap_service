from fastapi.testclient import TestClient

from unittest.mock import patch, Mock
from src.main import app

client = TestClient(app)


@patch("src.routers.api.get_org_ids_from_db", return_value=[1, 2, 3])
def test_get_org_ids(mocked_f):

    response = client.get("/api/org-ids")
    assert response.status_code == 200
    assert response.json() == [1, 2, 3]


@patch("src.routers.api.create_engine")
@patch("geopandas.read_postgis")
def test_read_data_no_data(mock_engine, mock_read):
    mock_gdf = Mock
    mock_gdf.empty = True
    mock_read.return_value = mock_gdf

    response = client.get("/api/data/5")
    assert response.status_code == 404


def test_read_data_invalid_orgid():

    response = client.get("/api/data/bla")
    assert response.status_code == 400
