import json
import conf.config as config
from elasticsearch import Elasticsearch, helpers
from elasticsearch.connection import create_ssl_context
from api import get, evoke_api
import re
import ssl
from pprint import pp

# This is a messy workaround to access without proper certs.
# TODO Test and then Implement CA certs on Production Instance.
context = create_ssl_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

user = config.ES_USR
pswd = config.ES_SEC

def checkauth():
    print(user, pswd)

es = Elasticsearch([{'host': '172.26.5.162', 'port': '9200'}],
                   scheme="https",
                   verify_certs=False,
                   ssl_context=context,
                   timeout=60,
                   http_auth=(user, pswd))


# Proofpoint API calls

# TODO PP calls need to use req.status_code == 200
def people(ep, *args):
    '''
    Creates a GET Request for the PP People API Endpoint
    And takes the Response and sends a POST Request to Elastic Search.
    '''
    req = get('pp', 'people', ep, args)
    # Note: Requests formats JSON unusually, so cast to text then us json loads
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
    endpoint = re.sub(r'(messages)|(clicks)', r'\1\2/', ep).lower()
    d = json.loads(get('pp', 'siem', endpoint).text)[ep]
    docs = [e for e in d if e]
    if docs:
        helpers.bulk(es, docs, index='pp_{}'.format(ep).lower())


def forensics(ep):
    '''
    Creates a GEt Request for the PP SIEM API Endpoint
    And takes the Response and sends a POST Request to Elastic Search.
    '''

    # Query for all messages blocked.
    q = es.search(
        index='*_messagesblocked',
        body={
            'query': {
                'match_all': {
                }
            }
        }
    )
    # Pull all the threatIDs from query, cast as set to remove duplicates.
    threat_ids = set([
        d['_source']['threatsInfoMap'][0]['threatID']
        for d in q['hits']['hits']
        ])

    # If there is a threat it, call forensics endpoint.
    # Store response in doc list.
    doc = [json.loads(get('pp', ep, None, threat).text)
           for threat in threat_ids if threathreat]
    # for threat in threat_ids:
    #    req = get('pp', ep, None, threat)
    #    d = json.loads(req.text)
    #    doc.append(d)

    # doc is not empty, bulk upload to elastic search:
    if doc:
        helpers.bulk(es, doc, index='pp_{}'.format(ep).lower())


# Sophos API calls


def so_endpoints():
    '''
    Collects endpoints across all tenants within the default time frame.
    Returns an ElasticSearch document which is injested by ES.

    Sophos does not expose this api at the global level, instead the endpoint API
    can only return endpoints for a given tenant. Each tenant has an ID which must
    be authenticated against in order to prove the tenant is associated with a
    a given Orgnization ID.

    Authentication is handled in the Sophos module.
    '''
    # TODO Determin the best time frame for the siem.
    def endpoints(site):
        '''
        Takes a tenant name, or site, and calls the endpoint API.
        Returns a GET request response.
        '''
        return get('sophos', 'tenant', None, tenant=site.id)

    # Get a map of each site in the system and issue GET request.
    sites = evoke_api('sophos', 'tenants')
    responses = [endpoints(sites.get(s)) for s in sites]

    # Get a list of data on each endpoint.
    for r in responses:
        doc = []
        if r.status_code == 200:
            d = json.loads(r.text)
            data = {}
            for i in d['items']:
                hostname = i.pop('hostname')
                data[hostname] = i
                doc.append(data)

            helpers.bulk(es, doc, index='so_endpoints_test')
