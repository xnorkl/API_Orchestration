import configparser
from os import environ, path
from dotenv import load_dotenv


# Get .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Proofpoint Config
PP_URL = 'https://tap-api-v2.proofpoint.com/v2/siem/'
PP_KEY = environ.get('PROOFPOINT_API_KEY')
PP_SEC = environ.get('PROOFPOINT_API_SECRET')
