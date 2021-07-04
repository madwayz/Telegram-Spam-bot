import os

TOKEN = os.environ.get('TOKEN')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database/accounts')
DATABASE = {
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "host": os.environ.get("POSTGRES_HOST"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "port": os.environ.get("POSTGRES_PORT", "5432")
}
REDIS_HOST = os.environ.get('REDIS_HOST')