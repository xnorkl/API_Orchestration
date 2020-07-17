import sqlite3
import json
import sys
import re

from caller import get

def access(db='./db/monophony.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    return conn, c

def purge():
    conn, c = access()

    c.execute("PRAGMA writable_schema = 1")
    c.execute("delete from sqlite_master where type in ('table','index', 'trigger')")
    c.execute("PRAGMA writeable_schema = 0")
    conn.commit()

    c.execute("VACUUM")
    conn.commit()

    try:
        c.execute("PRAGMA INTEGRITY_CHECK")
        conn.commit()
    except Exception as e:
        print(e)

    conn.close()



def people(ep, *args):
    ''' Takes endpoint and options and calls the endpoint api, stores response in db. '''
    conn, c = access()

    try:
        c.execute("SELECT count(name) FROM sqlite_master Where type='table' AND name='{}'".format(ep))
        if c.fetchone()[0]==1:
            c.execute("CREATE TABLE {} (guid TEXT, email TEXT, data JSON)".format(ep))
    except Exception as e:
        print(e)
    else:
        c.execute("CREATE TABLE {} (guid TEXT , email TEXT, data JSON)".format(ep))



    #c.execute("DROP TABLE {}".format(ep))
    m = get('pp','people', ep , args)
    d = json.loads(m.text)
    print(d)
    for i in d['users']:
        c.execute("insert into {} values (?, ?, ?)".format(ep),
            [i['identity']['guid'], i['identity']['emails'][0], json.dumps(i)]
        )
        conn.commit()

    conn.close()

def siem(ep,*args):
    conn, c = access()

    c.execute("SELECT count(name) FROM sqlite_master Where type='table' AND name='{}'".format(ep))
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
