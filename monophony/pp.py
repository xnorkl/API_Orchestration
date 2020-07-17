from enum import Enum

from utils.extra import lasthour

# Enumerate Proofpoint APIs and API calls.
# Enumerators are used similar to Haskell records.
# These may be removed for tuples or dicts...
Api = Enum('Api', {'SIEM': 'siem',
                   'People': 'people',
                   'Foresnics': 'forensics',
                   'Campaign': 'campaign'})

# TODO This needs to be handled differently....
SIEM = Enum('SIEM', {'Clicksblocked': 'clicks/blocked',
                     'Clickspermitted': 'clicks/permitted',
                     'Messagesblocked': 'messages/blocked',
                     'Messagesdelivered': 'messages/delivered',
                     'Issues': 'issues',
                     'Everything': 'all'})


# PP specific functions


def rooturl():
    return 'https://tap-api-v2.proofpoint.com/v2'


def threatid():
    # TODO: This needs to pull from a db to be effective.
    pass


def campaignid():
    # TODO: This needs to pull from a db to be effective.
    pass


def siem(i=lasthour(), f='json', t='url', s='active'):
    """ Returns a payload for the SIEM API.

    Parameters
    ----------

    Required:

    i (interval): time delta in ISO 8601 format
        A string containing an ISO8601-formatted interval.
        If this interval overlaps with previous requests for data,
        records from the previous request may be duplicated.
        The minimum interval is thirty seconds.
        The maximum interval is one hour.


    Optional:

    f (format): str
        A string specifying the format in which data is returned.
        If no format is specified, syslog will be used as the default.
        The following values are accepted:
        - syslog
        - json

    t (threatType): str
        A string specifying which threat type will be returned in the data.
        If no value is specified, all threat types are returned.
        The following values are accepted:
        - url
        - attachment
        - messageText

    s (threatStatus): str
        A string specifying which threat statuses will be returned in the data.
        If no value is specified, active and cleared threats are returned.
        The following values are accepted:
        - active
        - cleared
        - falsePositive

    """
    return {
        'format': f,
        'sinceTime': i,
        'threatType': t,
        'threatStatus': s
        }


def people(w=90, s=1000, p=1):
    """
    Takes an n-many days w, returns a Payload for the people API.

    Parameters
    ----------

    Required:

    w (window): int
        An integer indicating how many days the data should be retrieved for.
        Accepted values are 14, 30 and 90.


    Optional:

    s (size): int
        The maximum number of VAPs to produce in the response.
        The attackIndex value determine the order of results.
        Defaults to 1000.

    p (page): int
        The page of results to return, in multiples of the
        specified size (or 1000, if no size is explicitly chosen).
        Defaults to 1.
    """
    return {
        'window': w,
        'size': s,
        'page': p
    }


def forensics(t=True, i=False):
    """ Fetch forensic information for a given threat or campaign.

    Required:
    ---------
    At least one of

    t (threatId): bool
        Defaults to True. If True, return threatID(),
        if False, return campaignID().

    Optional:
    ---------

    i (includeCampaignForensics) : bool
        Defaults to False. May be used with the threatId parameter.
        If false, forensic data for threat identifier will be returned.
        If true AND if a threat has been associated with a campaign,
        forensic data for the entire campaign are returned.
        If true AND no threat has been assocaitaed with a campaign,
        forensic data for the individual threat are returned.
    """
    if t:
        return { 'threatId': threatid(), 'includeCampaignForensics': i }
    else:
        return { 'campaignID' : campaignid() }


def campaign():
    """ Returns a campaign ID. """
    return campaignid()
