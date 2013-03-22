# Download the Python helper library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient


# relys on TWILIO_AUTH_TOKEN and TWILIO_ACCOUNT_SID env variables
client = TwilioRestClient()
  
number = client.phone_numbers.get("PN3370cd26b57b0bf69e7bfce10c008a4b")
print number.phone_number

voiceURL = "http://twimlets.com/forward?PhoneNumber=319-743-8485&"

number.update(voice_url=voiceURL)
