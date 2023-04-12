import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASEDIR, '.env'))


POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB_NAME')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

# SECRET = os.environ.get('SECRET')
# PASSWORD = os.environ.get('PASSWORD')

# SMTP_USER = os.environ.get('SMTP_USER')
# SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
# SMTP_HOST = os.environ.get('SMTP_HOST')
# SMTP_PORT = os.environ.get('SMTP_PORT')

# REDIS_HOST = os.environ.get('REDIS_HOST')
# REDIS_PORT = os.environ.get('REDIS_PORT')
