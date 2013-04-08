from twilio.rest import TwilioRestClient
import datetime
from icalendar import Calendar
import urllib
from dateutil import tz

class Location:
    def __init__(self, info):
        self.info = info
        self.twilio_client = TwilioRestClient()
        self.forwarding_number_obj = self.twilio_client.phone_numbers.get(self.info["forwarding_number_id"])
        self.info['contact_list']['ResLife Office'] = "563-387-1330"
        
    def getInfo(self):
        return self.info

    def update(self):
        ''' checks for changes to the person on duty and makes necessary changes to forwarding info '''
        curr_forwarding_destinations,failNum = self.getCurrentForwardingDestinations()
            
        new_forwarding_destinations = []

        for name in self.getCurrentPersonsOnDuty():
            new_person_on_duty = name
            try:
                new_forwarding_destinations.append(self.info["contact_list"][new_person_on_duty.strip()])
            except KeyError:
                # TODO better handle this error
                new_forwarding_destinations.append("000-000-0000")

        if not curr_forwarding_destinations == new_forwarding_destinations:
            self.updateForwardingDestinations(new_forwarding_destinations, failNum)

    def updateForwardingDestinations(self, new_destination_numbers, failNumber):
        voice_URL = "http://twimlets.com/simulring?"
        incrementNum = 0;

        oldDestinationNumbers = self.getCurrentForwardingDestinations()

        for number in new_destination_numbers:
            voice_URL = voice_URL + "PhoneNumbers%5B" + str(incrementNum) + "%5D=" + number + "&"
            incrementNum = incrementNum + 1

            if not number in oldDestinationNumbers and self.info['send_sms']:
                to_number = "+1" + number.replace("-", "")  # +12316851234
                message = self.twilio_client.sms.messages.create(to=to_number, from_=self.forwarding_number_obj.friendly_name, body="You are now on duty.")

        voice_URL = voice_URL + "Message=Fowarded%20Call&" + "FailUrl=http://twimlets.com/forward?PhoneNumber=" + failNumber
        self.forwarding_number_obj.update(voice_url=voice_URL)

    def getTwilioNumber(self):
        return self.forwarding_number_obj.friendly_name

    def getCurrentForwardingDestinations(self): #Returns a tuple with the first element a list of simulring numbers
        #curently on call and the second item the fail number string
        current_numbers = []

        split_url = self.forwarding_number_obj.voice_url.split("=")
        for part in split_url:
            if str(part).__contains__("-"):
                current_numbers.append(str(part.split("&")[0]))
        fail_number = current_numbers.pop(current_numbers.__len__() - 1)
        return (current_numbers, fail_number)

    def getCurrentPersonsOnDuty(self):
        on_duty_names = []

        ics = urllib.urlopen(self.info["calendar_url"]).read()
        ical = Calendar.from_ical(ics)

        for vevent in ical.subcomponents:
            if vevent.name != "VEVENT":  # if it's not an event, ignore it
                continue

            start_date = vevent.get('DTSTART').dt #.strftime("%Y-%m-%d")  # .dt is a datetime or date
            end_date = vevent.get('DTEND').dt
            
            if isinstance(start_date, datetime.datetime):
                    # it's a datetime.datetime object (includes time)
                    start_date = start_date.astimezone(tz.tzlocal()) # convert to local time
                    end_date = end_date.astimezone(tz.tzlocal())
                    curr_date = datetime.datetime.now(tz.tzlocal())

            elif isinstance(start_date, datetime.date):
                    # it's a datetime.date object (does not include time)
                    curr_date = datetime.date.today()
                    end_date = end_date - datetime.timedelta(days=1)

                    if self.info["isResLife"] == True:
                        nowTime = datetime.datetime.now().time()
                        #nowTime = datetime.time(1,0,0)
                        midnightTime = datetime.time(23, 59, 59)
                        sevenPMTime = datetime.time(19,0,0)
                        eightAMTime = datetime.time(8,0,0)

                        if sevenPMTime <= nowTime or nowTime <= eightAMTime:
                            curr_date = curr_date - datetime.timedelta(days=1)
                        else:
                            return ["ResLife Office"]

            if start_date <= curr_date <= end_date: # if this event is right now
                    title = str(vevent.get('SUMMARY')) # this will be the title of the event (hopefully  name)

                    on_duty_names.append(title)
        
        # handle case where nobody is on duty calendar
        if len(on_duty_names) == 0:
            on_duty_names.append("ResLife Office")
        return on_duty_names


def testLocation():
    calendar_url= "http://www.google.com/calendar/ical/luther.edu_p5c373m13dppnsqeajcs4se5nc%40group.calendar.google.com/public/basic.ics"
    forwarding_number_id = "PN3370cd26b57b0bf69e7bfce10c008a4b"

    contact_list = {}
    contact_list["Isaac DL"] = "612-978-3683"
    contact_list["Austen Smith"] = "319-743-8485"

    info = {}
    info["location_name"] = "Brandt Hall"
    info["calendar_url"] = calendar_url
    info["forwarding_number_id"] = forwarding_number_id
    info["contact_list"] = contact_list
    info["isResLife"] = True

    location = Location(info)
    
    print location.getCurrentPersonsOnDuty()



#testLocation()
