# kmanagecore
'''
Copyright 2021 myKaarma

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

import requests

#Keys in the "creds" dict.
KEY_USERNAME = 'username'
KEY_PASSWORD = 'password'
KEY_BASE_URL = 'base_url' #kept so this code can be used in dev and QA as well, not just prod.


def get_dealer_associate_info(creds, dept_uid, dealerassociate_uid, DEBUG = False, SIMULATION = False):
    """A simple method to get the details of a single dealer associate.

    This method will take the credentials (username, password, and base URL)
    the departmentUUID, and the dealer associate UUID, and GET the 
    information for that dealer associate from the API. An optional DEBUG boolean 
    can be passed that will result in dumping of 
    the HTTP response on stdout. Another optional input SIMULATION, when set to true, will 
    lead to NO network traffic, just the dumping of the request.
    """

    url = "%s/department/dealerAssociate/list" % (creds[KEY_BASE_URL])
    request = dict()
    request["dealerAssociateUuids"] = [dealerassociate_uid]
    request["departmentUuids"] = [dept_uid]
    request["validate"] = False
    request["doNotValidate"] = True
    
    if SIMULATION:
        print("\n\n[SIM MODE] I would like to make a POST request to %s with data %s" % (url,request))
        return "SIMULATION MODE ON"
    else:
        r = requests.post(url,auth=(creds[KEY_USERNAME],creds[KEY_PASSWORD]),json = request)
        if DEBUG:
            print(r.json())
        return r.json()['dealerAssociates'][dealerassociate_uid]


if __name__ == "__main__":
    print('Sorry, no direct usage available. Import and then call the methods.')