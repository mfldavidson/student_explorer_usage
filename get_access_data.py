import pandas as pd
import numpy as np
import json
from creds import APIUTILTEST # Get the ApiUtil object for the Umich Test API
from get_db_data import dbusers # Get the DataFrame of users from local DB

# Call the API for the M-Community group that controls access to SE
group_url = 'MCommunityGroups/Members/Student%20Explorer%20Users'
resp = APIUTILTEST.api_call(group_url, 'mcommunitygroups')
resp_json = json.loads(resp.text) # Load the response into a dictionary

# Get a list of uniqnames for users who currently have access to SE
group_data = resp_json[u'MCommunityInfo'][u'MCommunityGroupData']
b_members = group_data[u'MemberList'].encode('utf-8') # Comma-separated bytes object
member_list = b_members.decode().split(',') # List of uniqnames with access

# Create a df of members with 'active' set to True for all
members = pd.DataFrame({'uniqname': member_list,
                        'active': True})

# Merge members with dbusers so we know which users are active
users = dbusers.merge(members, on='uniqname', how='outer')

# Set all NA values in is_staff, is_superuser, active to False
bool_cols = users.columns[-3:] # Get an index object of the columns
users[bool_cols] = users[bool_cols].fillna(False)
