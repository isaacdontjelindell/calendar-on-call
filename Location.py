__author__ = 'isaac'

from DutyCalendar import DutyCalendar
from ForwardingNumber import ForwardingNumber
from ContactList import ContactList

class Location:
    def __init__(self, location_name, duty_calendar, contact_list, forwarding_number):

        self.location_name = location_name  # description of this location (e.g. "Brandt Hall")
        self.duty_calendar = duty_calendar  # DutyCalendar for this location
        self.contact_list = contact_list    # ContactList containing the phone numbers for this location
        self.forwarding_number = forwarding_number  # Twilio ForwardingNumber for this location

        self.current_on_call = "Not A. Person"  # name of person currently on call

    def update(self):
        ''' checks for changes to the person on duty and makes necessary changes to forwarding info '''
        new_on_call = self.duty_calendar.getCurrentOnCall()[0]  # for now just using the first entry on duty - TODO handle multiple

        if not new_on_call == self.current_on_call:
            self.current_on_call = new_on_call
            new_number = self.contact_list.getNumber(new_on_call)
            self.forwarding_number.updateForwardingDestination(new_number)
            print (self.current_on_call + " is now on duty. Calls will be forwarded to " + new_number + ".")


def testLocation():
    cal = DutyCalendar("http://www.google.com/calendar/ical/luther.edu_p5c373m13dppnsqeajcs4se5nc%40group.calendar.google.com/public/basic.ics")
    num = ForwardingNumber("PN3370cd26b57b0bf69e7bfce10c008a4b")

    dct = {}
    dct["Isaac DL"] = "612-978-3683"
    dct["Austen Smith"] = "123-456-7891"
    contact_list = ContactList(dct)

    location = Location("Brandt", cal, contact_list, num)
    print num.getCurrentForwardingDestination()

    location.update()
    print num.getCurrentForwardingDestination()

#testLocation()