import json
import requests
from elasticsearch import Elasticsearch, helpers
from api import get
from ssl import create_default_context

context = create_default_context(cafile='./conf/certs/es.crt')
context.check_hostname = False

# res = requests.get('http://192.168.164.113:9200')
es = Elasticsearch([{'host': '192.168.164.113', 'port': '9200'}],
                   use_ssl=True,
                   http_auth=('elastic', 'PVV26ZleXglLv4wlRYEU'),
                   ssl_context=context)


def people(ep, *args):
    req = get('pp', 'people', ep, args)
    print(req)
    d = json.loads(req.text)

    # Send data to elasticsearch if populated.
    docs = []
    for x in d['users']:
        doc = {'email': x['identity']['emails'],
               'attackIndex': x['threatStatistics']['attackIndex']}
        docs.append(doc)

    helpers.bulk(es, docs, index='proofpoint_vap')
    helpers.bulk

people('vap', 14)
