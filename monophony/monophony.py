from calls.db import people, siem

def main():
    db.people()
    db.siem(ep='clicksBlocked')
    #siem(ep='clicksPermitted')
    #siem(ep='messagesBlocked')
    #siem(ep='messagesDelivered')


if __name__ == "__main__":
    main()
