#list-appointments.py
'''
Copyright 2020 myKaarma

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from optparse import OptionParser
from mkauth import username, password, appt_base_url, manage_base_url
import kappointmentcore, kmanagecore

appt_creds = {kappointmentcore.KEY_USERNAME:username, kappointmentcore.KEY_PASSWORD:password, kappointmentcore.KEY_BASE_URL:appt_base_url}

manage_creds = {kmanagecore.KEY_USERNAME:username, kmanagecore.KEY_PASSWORD:password, kmanagecore.KEY_BASE_URL:manage_base_url}

import pprint


# Global, set to true by the parser if needed
DEBUG = False
SIMULATION = False
# cache for users. For re-use
USER_CACHE = dict()

def prettyprint(message, width=280):
    '''pretty prints the text'''
    pprint.pprint(message,width = width)

def debug_print(message):
    '''Prints the message if the DEBUG flag is set'''
    if DEBUG:
        prettyprint(message)


def get_dealer_associate_info(dept_uid,dealer_associate_uuid):
    """Gets the details of a given dealer associate"""
    global USER_CACHE
    debug_print("getting DA for UUID %s" % dealer_associate_uuid)
    if dealer_associate_uuid == None:
        return None
    else:
        #check cache
        if dealer_associate_uuid in USER_CACHE:
            debug_print("cache hit for %s" % dealer_associate_uuid)
            return USER_CACHE[dealer_associate_uuid]
        else:
            debug_print("cache miss for %s" % dealer_associate_uuid)
            found_da = kmanagecore.get_dealer_associate_info(manage_creds, dept_uid, dealer_associate_uuid, DEBUG = DEBUG, SIMULATION = SIMULATION)
            if found_da != None:
                USER_CACHE[dealer_associate_uuid] = found_da
            return found_da


def list_appointments(dept_uid, date_str):
    """Lists all appointments at the dept_uid on the given date"""
    appointments = kappointmentcore.list_appointments(appt_creds, dept_uid, date_str, DEBUG = DEBUG, SIMULATION = SIMULATION)
    if SIMULATION:
        return "Simulation mode; not looking for DA info"
    else:
        for a in appointments:
            debug_print(a)
            assignedDA = get_dealer_associate_info(dept_uid, a['assignedAdvisorUuid'])
            creatorDA = get_dealer_associate_info(dept_uid, a['creatorAdvisorUuid'])
            a['assignedAdvisor'] = assignedDA
            a['creatorAdvisor'] = creatorDA
        return appointments
 
    
def main():
    global DEBUG #important, otherwise the global var DEBUG won't be set.
    global SIMULATION #important, otherwise the global var SIMULATION won't be set.
    
    usage = "usage: python3 %prog [-v|--verbose] [-s|--simulation] --date YYYY-MM-DD --department abcd1234 >> out.log"
    parser = OptionParser(usage)
    parser.add_option("-t", "--date", dest="date_str",
                      help="get appointments for DATE")
    parser.add_option("-d", "--department", dest="dept_uid",
                      help="get appointments for DEPT")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    parser.add_option("-s", "--simulation",
                      action="store_true", dest="simulation")
    (options, args) = parser.parse_args()
    DEBUG = options.verbose
    SIMULATION = options.simulation
    
    if options.date_str == None:
        parser.error("missing date")
    if options.dept_uid == None:
        parser.error("missing department")
    debug_print('# Listing appointments now')
    prettyprint(list_appointments(options.dept_uid,options.date_str))

if __name__ == "__main__":
    main()