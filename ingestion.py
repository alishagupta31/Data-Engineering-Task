import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from sqlalchemy.exc import IntegrityError
import logging
import argparse

from constants import DATABASE, SCHEMA_NAME, CONFIG_PATH, TABLE_NAME, CITIES, DB_CONNECTION_URL
from utility.utils import load_config, get_database_engine

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_cities_table(engine, schema_name):
    """Creates cities DataFrame and inserts it into the database."""
    logger.info("Creating cities DataFrame...")

    cities_df = pd.DataFrame.from_dict(
        {city_name: {"city_name": city_name, "latitude": coords["latitude"], "longitude": coords["longitude"]}
         for city_name, coords in CITIES.items()},
        orient='index'
    )

    try:
        # Insert cities into the specified schema
        cities_df.to_sql('cities', engine, if_exists='append', index=False, schema=schema_name)
        logger.info("Cities table created and data inserted successfully.")
    except IntegrityError:
        logger.warning("Cities already exist in the database.")


def fetch_cloud_cover_data(city, openmeteo):
    """Fetch cloud cover data for a given city using the Open-Meteo client."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": city['latitude'],
        "longitude": city['longitude'],
        "hourly": ["cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
        "start_date": city['start_date'],  # Use city's start_date
        "end_date": city['end_date']  # Use city's end_date
    }

    api_response = openmeteo.weather_api(url, params=params)[0]
    return api_response

def process_cloud_cover_data(openmeteo, cities, engine, schema_name, table_name):
    """Fetch and process cloud cover data for all cities."""
    cloud_cover_data_list = []

    for city_name, city_coords in cities.items():
        try:
            response = fetch_cloud_cover_data(city_coords, openmeteo)
            logger.info(f"Processing data for {city_name}...")

            # Process hourly data
            hourly = response.Hourly()
            hourly_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left"
                ),
                "cloud_cover": hourly.Variables(0).ValuesAsNumpy(),
                "cloud_cover_low": hourly.Variables(1).ValuesAsNumpy(),
                "cloud_cover_mid": hourly.Variables(2).ValuesAsNumpy(),
                "cloud_cover_high": hourly.Variables(3).ValuesAsNumpy(),
                "city_name": city_name
            }

            cloud_cover_data_list.append(pd.DataFrame(data=hourly_data))

        except Exception as e:
            logger.error(f"Error processing data for {city_name}: {e}")

    # Combine all DataFrames into one and insert into database
    if cloud_cover_data_list:
        cloud_cover_df = pd.concat(cloud_cover_data_list, ignore_index=True)
        try:
            # Insert cloud cover data into the specified schema and table
            cloud_cover_df.to_sql(table_name, engine, if_exists='append', index=False, schema=schema_name)
            logger.info("Cloud cover data inserted successfully.")
        except IntegrityError:
            logger.warning("Cloud cover data already exists in the database.")

def main(config_path):
    # Load configuration
    config = load_config(config_path)

    # Database connection
    db_connection_url = config[DATABASE]['db_connection_url']
    cities = config['cities']
    schema_name = config[SCHEMA_NAME]
    table_name = cities[TABLE_NAME]  # Get table name from config

    # Create database engine using the new function
    engine = get_database_engine(DB_CONNECTION_URL)

    create_cities_table(engine, schema_name)

    # Setup the Open-Meteo API client with cache and retry
    logger.info("Setting up the Open-Meteo API client with cache and retry...")
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    process_cloud_cover_data(openmeteo, cities, engine, schema_name, table_name)

if __name__ == "__main__":
    # Argument parser to get config path from command line
    parser = argparse.ArgumentParser(description='Process cloud cover data.')
    parser.add_argument(CONFIG_PATH, type=str, help='Path to the YAML configuration file')
    args = parser.parse_args()

    main(args.config_path)