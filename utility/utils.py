import logging

import yaml
from sqlalchemy import create_engine

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