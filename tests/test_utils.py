from sqlalchemy import create_engine

import pytest
from src.utils import wait_for_db, write_data_to_db
from unittest.mock import Mock, patch
import pandas as pd

TEST_STR = "test"

@pytest.fixture
def temp_data(tmp_path):
    test_data = pd.DataFrame(
    {'id': [1, 2, 3],
        'false_name': ['Point(0, 0)', 'Point(1, 1)', 'Point(2, 2)']
        }
    )

    temp_dir = tmp_path / "sub"
    temp_dir.mkdir()
    temp_path = temp_dir / "hello.csv"
    test_data.to_csv(temp_path)
    return temp_path

def test_wait_for_db():
    # Create an engine pointing to a non-existent database
    engine = create_engine('postgresql://user:password@localhost:5432/non_existent_db')

    with pytest.raises(TimeoutError):
        wait_for_db(engine, timeout=1)


@patch('src.utils.should_create_table', return_value=False)
def test_write_data_to_db_should_create_table_return_early(mock_f):
    mock_engine = Mock()
    # expecting early return since we should not write to db
    assert not write_data_to_db(mock_engine, TEST_STR, TEST_STR, TEST_STR)

@patch('src.utils.should_create_table', return_value=True)
@patch('src.config.settings')
def test_write_data_to_db_invalid_column(mock_f, mock_settings, temp_data):
    mock_settings.DATA_SOURCE = temp_data

    mock_engine = Mock()
    with pytest.raises(KeyError):
        write_data_to_db(mock_engine, temp_data, TEST_STR, TEST_STR)