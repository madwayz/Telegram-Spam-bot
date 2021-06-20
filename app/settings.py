import os

TOKEN = os.environ.get('TOKEN')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database/accounts')