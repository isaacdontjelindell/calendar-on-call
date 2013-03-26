__author__ = 'isaac'


class ContactList:
    def __init__(self, contact_dict):
        ''' contact dict should be keyed by name: "name":"xxx-xxx-xxxx" '''
        self.contact_dict = contact_dict

    def getNumber(self, name):
        ''' name is a string '''
        return self.contact_dict[name]


def testContactList():
    dct = {}
    dct["Isaac DL"] = "612-978-3683"
    dct["Austen Smith"] = "123-456-7891"

    cl = ContactList(dct)

    print cl.getNumber("Isaac DL")

# testContactList()