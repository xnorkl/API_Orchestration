import dbhandler as db

def main():
    # TODO Main should read from a config file take arguments.
    db.people('vap', 14)
    db.siem(ep='clicksBlocked')
    db.siem(ep='clicksPermitted')
    db.siem(ep='messagesBlocked')
    db.siem(ep='messagesDelivered')


if __name__ == "__main__":
    main()
