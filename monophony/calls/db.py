import sqlite3
import json
import sys
import re

from caller import get

def access(db='monophony.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    return conn, c

def people(*args):
    conn, c = access()

    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='vap' ''')
    if not c.fetchone()[0]==1:
        c.execute("CREATE TABLE vap (guid TEXT , email TEXT, data JSON)")

    m = get('pp','people','vap')
    d = json.loads(m.text)
    for i in d['users']:
        c.execute("insert into vap values (?, ?, ?)",
            [i['identity']['guid'], i['identity']['emails'][0], json.dumps(i)]
        )
        conn.commit()

    conn.close()

def siem(ep,*args):
    conn, c = access()

    c.execute(''' SELECT count(name) FROM sqlite_master Where type='table' AND name='{}' '''.format(ep))
    if not c.fetchone()[0]==1:
        c.execute("Create TABLE {} (messageID TXT, fromAddress TXT, data JSON)".format(ep))
    endpoint = re.sub(r'(messages)|(clicks)', r'\1\2/', ep).lower()
    m = get('pp', 'siem', endpoint)
    d = json.loads(m.text)
    for i in d[ep]:
        c.execute("insert into {} values (?, ?, ?)".format(ep),
            [ i['GUID'], ''.join(i['fromAddress']), json.dumps(i)]
        )
        conn.commit()
    conn.close()

def cycle():
    conn, c = access()
    conn.close()

people()
