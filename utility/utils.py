import logging
import os

import yaml
from sqlalchemy import create_engine

from constants import DATABASE, DB_CONNECTION_URL, DB_USERNAME, DB_PASSWORD

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path):
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_database_engine(db_connection_url):
    """Create and return a database engine."""
    logger.info("Creating database engine...")
    return create_engine(db_connection_url)

def get_db_connection_string(config):
    """
    Constructs the database connection string from the config and environment variables.

    Args:
        config (dict): The configuration dictionary containing the connection URL template.

    Returns:
        str: The formatted database connection string.
    """
    # Get environment variables for username and password
    db_username = os.getenv(DB_USERNAME)
    db_password = os.getenv(DB_PASSWORD)

    # Extract connection URL template from config
    db_connection_url_template = config[DATABASE][DB_CONNECTION_URL]

    # Replace placeholders with environment variables
    db_connection_url = db_connection_url_template.format(username=db_username, password=db_password)

    return db_connection_url
