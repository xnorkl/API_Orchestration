from os import environ, path
from dotenv import load_dotenv


# Get .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


# Elastic Stack Config
ES_USR = environ.get('ELASTIC_USER')
ES_SEC = environ.get('ELASTIC_PASS')


# Proofpoint Config
PP_URL = 'https://tap-api-v2.proofpoint.com/v2'
PP_KEY = environ.get('PROOFPOINT_API_KEY')
PP_SEC = environ.get('PROOFPOINT_API_SECRET')


# Sophos Config
SO_JWT = 'https://id.sophos.com/api/v2/'
SO_KEY = environ.get('SOPHOS_API_KEY')
SO_SEC = environ.get('SOPHOS_API_SECRET')
