import eshandler as es


def main():
    # TODO Main should read from a config file take arguments.
    print("hello")
    es.people('vap', 14)
    es.siem(ep='clicksBlocked')
    es.siem(ep='clicksPermitted')
    es.siem(ep='messagesBlocked')
    es.siem(ep='messagesDelivered')
    es.forensics(ep='forensics')


if __name__ == "__main__":
    main()
