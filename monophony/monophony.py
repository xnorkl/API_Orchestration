import sys
sys.path.append('./calls/')

from db import people, purge, siem
def main():
    purge()
    people('vap', 14)
    siem(ep='clicksBlocked')
    siem(ep='clicksPermitted')
    siem(ep='messagesBlocked')
    siem(ep='messagesDelivered')


if __name__ == "__main__":
    main()
