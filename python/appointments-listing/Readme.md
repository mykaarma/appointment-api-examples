# Listing all appointments for a single day for a given store
This program takes two inputs: 
- the UUID of the department, and 
- the date for which we need the appointments.

The code then iterates through the appointments of the day, and also enriches the user information.

# Dependencies
- python3
- optparse
- pprint
- requests

# Scopes Needed
- `appointment.get`, at the department level.
- `manage.dealerassociate.read`, at the department level
- 

# Authentication
- save creds in mkauth.py (created by making a copy of mkauth.py.sample). Do NOT commit this file.

# How to run
```
python3 list-appointments.py --date YYYY-MM-DD --department abcd1234 >> out.log
```