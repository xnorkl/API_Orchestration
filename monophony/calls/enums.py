from enum import Enum
# Enumerate APIs
class app(Enum):
    PP = 'pp'
    SO = 'sophos'
    FP = 'forcepoint'
    SP = 'sharepoint'
    O3 = 'office365'
    AZ = 'azure'

# Enumerate Proofpoint APIs and API calls.
class pp(Enum):
    def __str__(self):
        return self.value

    SIEM = 'siem'
    People = 'people'
    Forensics = 'forensics'
    Campaign = 'campaign'

class siemendpoint(Enum):
    Clicksblocked = 'clicks/blocked'
    Clickspermitted = 'clicks/permitted'
    Messagesblocked = 'messages/blocked'
    Messagesdelivered = 'messages/delivered'
    Issues = 'issues'
    Everything = 'all'

class peopleendpoint(Enum):
    Vap = 'vap'
