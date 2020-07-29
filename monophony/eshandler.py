import json
import conf.config as config
from elasticsearch import Elasticsearch, helpers
from elasticsearch.connection import create_ssl_context
from api import get
import re
import ssl


# This is a messy workaround to access without proper certs.
# TODO Test and then Implement CA certs on Production Instance.
context = create_ssl_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

user = config.ES_USR
pswd = config.ES_SEC

es = Elasticsearch([{'host': '192.168.164.115', 'port': '9200'}],
                   scheme="https",
                   verify_certs=False,
                   ssl_context=context,
                   timeout=60,
                   http_auth=(user, pswd))


def people(ep, *args):
    '''
    Creates a GET Request for the PP People API Endpoint
    And takes the Response and sends a POST Request to Elastic Search.
    '''
    req = get('pp', 'people', ep, args)
    d = json.loads(req.text)
    if d:

        # Send data to elasticsearch if populated.
        docs = []
        for e in d['users']:
            doc = {'email': e['identity']['emails'],
                   'attackIndex': e['threatStatistics']['attackIndex']}
            docs.append(doc)

        helpers.bulk(es, docs, index='proofpoint_vap')


def siem(ep, *args):
    '''
    Creates a GET Request for the PP SIEM API Endpoint
    And takes the Response and sends a POST Request to Elastic Search.
    '''
    endp = re.sub(r'(messages)|(clicks)', r'\1\2/', ep).lower()
    req = get('pp', 'siem', endp)
    print(req.url)

    d = json.loads(req.text)
    print(d)
    if d:

        # Send data to elasticsearch if populated
        docs = []
        for e in d[ep]:
            docs.append(e)

        helpers.bulk(es, docs, index='pp_{}'.format(ep).lower())


def forensics(ep):
    '''
    Creates a GEt Request for the PP SIEM API Endpoint
    And takes the Response and sends a POST Request to Elastic Search.
    '''

    q = es.search(
        index='*_messagesblocked',
        body={
            'query': {
                'match_all': {
                }
            }
        }
    )

    t_ids = set([
        d['_source']['threatsInfoMap'][0]['threatID']
        for d in q['hits']['hits']
        ])
    doc = []
    for t_id in t_ids:
        req = get('pp', ep, None, t_id)
        d = json.loads(req.text)
        doc.append(d)
    if d:
        helpers.bulk(es, doc, index='pp_{}'.format(ep).lower())
