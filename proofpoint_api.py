import sys
import datetime
import json
import requests
import pprint

'''Proofpoint API request. Returns JSON output. '''

# Credentials are generated at the TAP server.

PRINCIPAL = "a737f3cb-8c8e-d873-086b-270540dcab5d"
SECRET =  "f298519077c461d214e9b615e8c3515e35f5b1079a73c90f62caacf9ddacddf0"

# Get past date in ISO 8601 format. Pull reports in the last hour or 3600.00s seconds.

now = datetime.datetime.utcnow()
min_delta = now - datetime.timedelta(seconds=3600)
last_hour =  min_delta.replace(microsecond=0).isoformat() + 'Z'
# Generate URL Requests

# SIEM

siem_payload = {
    'format':'json',
    'sinceTime': last_hour,
    'threatStatus': ['active','cleared']
    }

siem_r = requests.get(
    'https://tap-api-v2.proofpoint.com/v2/siem/all',
    params=siem_payload,
    auth=(PRINCIPAL,SECRET)
    )

forensics_payload = {
    'threatId' : '671814f49dce70230831baa15a2cf8991d5194d9e05a1ff2266349b593c1dd67'
    '



response=siem_r.json()

with open('data.json', 'a') as outfile:
  json.dump(response, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

# Campaign

print(response)





#print(siem_r.text)
