# Download the Python helper library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient


class ForwardingNumber():

    # numberId is the PNxxxxxxxxxxxxxx
    def __init__(self, forwarding_number_id):
        self.twilio_client = TwilioRestClient()
        self.forwarding_number_id = forwarding_number_id
        self.forwarding_number_obj = self.twilio_client.phone_numbers.get(forwarding_number_id)

    # newDestinationNumber must be xxx-xxx-xxxx
    def updateForwardingDestination(self, new_destination_number):
        voice_URL = "http://twimlets.com/forward?PhoneNumber=" + new_destination_number + "&"
        self.forwarding_number_obj.update(voice_url=voice_URL)
        return True

    def getCurrentForwardingDestination(self):
        return self.forwarding_number_obj.voice_url.split("=")[1].strip("&")



def testForwardingNumber():
    num = ForwardingNumber("PN3370cd26b57b0bf69e7bfce10c008a4b")

    print num.getCurrentForwardingDestination()
    num.updateForwardingDestination("612-978-3683")

    print num.getCurrentForwardingDestination()
    num.updateForwardingDestination("319-743-8485")

# testForwardingNumber()