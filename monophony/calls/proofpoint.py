import datetime
from enum import Enum
import requests
import re
from abc import ABC, ABCMeta, abstractmethod
import config as conf

# Enumerate APIs.
class api(Enum):
    SIEM = 'siem'
    People = 'people'
    Forensics = 'forensics'
    Campaign = 'campagn'

# Enumerate calls for the siem api.
class event(Enum):
    clickblocked = 'clicks_blocked'
    clickspermitted = 'clicks_permitted'
    messagesblocked = 'messages_blocked'
    messagesdelivered = 'messages_delivered'
    issues = 'issues'
    everything = 'all'


def delta_t():
    ''' Return last hour in ISO 8601 format. '''

    now = datetime.datetime.utcnow()
    min_delta = now - datetime.timedelta(seconds=3600)
    return min_delta.replace(microsecond=0).isoformat() + 'Z'


class Request(object, metaclass=ABCMeta):
    ''' Abstract API Class. '''
    def __init__(self):
        self.apicall = self.rooturl()
        self.apicred = self.credentials()
        self.tperiod = delta_t()
        super().__init__()

    @abstractmethod
    def rooturl(self):
        pass

    @abstractmethod
    def credentials(self):
        pass

class Proofpoint(Request):
    '''Proofpoint API request. Returns JSON output. '''

    def rooturl(self):
        return (conf.PP_URL)

    def credentials(self):
        return (conf.PP_KEY, conf.PP_SEC)

    # Generate API Payloads #
    def siem(self, call):
        siem_payload = {
            'format': 'json',
            'sinceTime': self.tperiod,
            'threatStatus': ['active']
        }

        url = self.apicall + 'siem/'
        if call is event.clickblocked:
            url += 'clicks/blocked'
        elif call is event.clickspermitted:
            url += 'clicks/permitted'
        elif call is event.messagesblocked:
            url += 'messages/blocked'
        elif call is event.messagesdelivered:
            siem_url += 'messages/delivered'
        elif call is event.issues:
            siem_url += 'issues'
        elif call is event.everything:
            siem_url += 'all'
        else:
            raise TypeError('call must be an instance of siem_call enum')

        # Invoke HTML GET Request with the construscted payload.
        return requests.get(url,params=siem_payload,auth=self.apicred)

    def forensics(self):
        ''' Defines a payload provided by the Forensics API. Returns JSON '''

        forensics_payload = {
            'threatId': '671814f49dce70230831baa15a2cf8991d5194d9e05a1ff2266349b593c1dd67'
        }

        forensics_r = requests.get(
            'https://tap-api-v2.proofpoint.com/v2/forensics',
            params=forensics_payload,
            auth=(PRINCIPAL, SECRET)
        )
        return forensics_r.json()

    def people(self):
        ''' Defines a payload provided by the Poeple API. Returns JSON.'''

        people_payload = {'window': 90}

        people_r = requests.get(
            'https://tap-api-v2.proofpoint.com/v2/people/vap',
            params=people_payload,
            auth=(PRINCIPAL, SECRET)
        )
        return siem_r.json()

    ## Create Reports from API Requests ##

    @staticmethod
    def blocklist(pp):
        ''' Defines a Blocklist. Returns a List of formatted Text '''
        #TODO: Add more checks.
        T = last_hour()
        CALL = siem_call.messages_blocked
        blocked = pp.siem(CREDS, URL, CALL, T)
        for report in blocked['messagesBlocked']:
            if report['fromAddress'][0] != report['toAddresses'][0]:
                m = re.search(
                    r"[a-zA-Z0-9_\-\.]+@[a-zAA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}",
                    report['headerFrom']
                )
                if m:
                    from_addr = m[0]
                else:
                    from_addr = "None"
                to_addr = [a for a in report['toAddresses']]
                d = {
                    'from': from_addr,
                    'to': to_addr,
                    'sender IP': report['senderIP'],
                    'threat': report['threatsInfoMap'][0]['threat'],
                    'threatID': report['threatsInfoMap'][0]['threatID']
                }
            return [ "{} : {}".format(k, v) for k, v in d.items()]

    @staticmethod
    def vap(pp):
        people_reports = people_r.json()
        for user in people_reports['users']:
            return user['identity']['emails'][0]


pp = Proofpoint()
call = event.clickblocked
report = pp.siem(call)

print(report)
#       answer = str(report['fromAddress'][0]) + '\n'
#       with open("blocklist.txt", 'a') as outfile:
#           outfile.write(answer)


# If we want to store JSON, then we can do this...

# Write to and output
# responses=[siem_r.json(),forensics_r.json()]
# stores=['siem.json','forensics.json']
#i = 0
# for response in responses:
#    with open(stores[i], 'a') as outfile:
#        json.dump(response, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
#    i = i + 1
