import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pandas as pd

from ingestion import create_cities_table, fetch_cloud_cover_data, process_cloud_cover_data, main

# Test data
CITIES = {
    "Test City": {"city_name": "Test City", "latitude": 35.6895, "longitude": 139.6917, "start_date": "2024-01-01",
                  "end_date": "2024-01-02"}
}


@pytest.fixture
def mock_engine():
    # Mock SQLAlchemy engine
    return MagicMock()


@pytest.fixture
def mock_openmeteo():
    # Mock Open-Meteo client
    client = MagicMock()
    client.weather_api.return_value = [
        {
            "Hourly": {
                "Time": lambda: [1609459200],  # Start date as a timestamp
                "TimeEnd": lambda: [1609462800],  # End date as a timestamp
                "Interval": lambda: 3600,
                "Variables": lambda idx: MagicMock(ValuesAsNumpy=lambda: [50])
            }
        }
    ]
    return client


def test_create_cities_table(mock_engine):
    with patch("ingestion.pd.DataFrame.to_sql") as mock_to_sql:
        create_cities_table(mock_engine, "test_schema")
        mock_to_sql.assert_called_once_with(
            'cities', mock_engine, if_exists='append', index=False, schema="test_schema"
        )


def test_create_cities_table_integrity_error(mock_engine):
    # Create a mock IntegrityError with required parameters
    integrity_error = IntegrityError("statement", "params", "orig")

    # Simulate IntegrityError
    with patch("ingestion.pd.DataFrame.to_sql", side_effect=integrity_error):
        with patch("ingestion.logger.warning") as mock_logger:
            create_cities_table(mock_engine, "test_schema")
            mock_logger.assert_called_once_with("Cities already exist in the database.")


def test_fetch_cloud_cover_data(mock_openmeteo):
    city = {"latitude": 35.6895, "longitude": 139.6917, "start_date": "2024-01-01", "end_date": "2024-01-02"}
    data = fetch_cloud_cover_data(city, mock_openmeteo)

    assert data == mock_openmeteo.weather_api.return_value[0]
    mock_openmeteo.weather_api.assert_called_once_with(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": 35.6895,
            "longitude": 139.6917,
            "hourly": ["cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
            "start_date": "2024-01-01",
            "end_date": "2024-01-02"
        }
    )


def test_process_cloud_cover_data_error(mock_openmeteo, mock_engine):
    # Simulate an error in fetch_cloud_cover_data
    with patch("ingestion.fetch_cloud_cover_data", side_effect=Exception("Error in API")):
        with patch("ingestion.logger.error") as mock_logger:
            process_cloud_cover_data(mock_openmeteo, CITIES, mock_engine, "test_schema", "cloud_cover_table")
            mock_logger.assert_called_with("Error processing data for city_name: Test City: Error in API")


def test_main():
    # Mock dependencies in main function
    mock_config = {
        "cloud_cover_data": {
            "cities": CITIES,
            "table_name": "cloud_cover_table"
        },
        "schema_name": "test_schema"  # Ensure this key exists
    }

    with patch("ingestion.load_config", return_value=mock_config):
        with patch("ingestion.get_db_connection_string", return_value="postgresql://user:password@localhost/dbname"):
            with patch("ingestion.get_database_engine", return_value=MagicMock()):
                with patch("ingestion.create_cities_table") as mock_create_cities:
                    with patch("ingestion.process_cloud_cover_data") as mock_process_data:
                        main("config.yaml")
                        mock_create_cities.assert_called_once()
                        mock_process_data.assert_called_once()
