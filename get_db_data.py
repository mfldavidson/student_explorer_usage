import pymysql # For connecting to the Student Explorer MySQL database
import pandas as pd
import numpy as np
from creds import mysqlcreds # Get the database credentials stored in creds.py

# Connect to the database
conmysql = pymysql.connect(mysqlcreds['host'],
                      port=mysqlcreds['port'],
                      user=mysqlcreds['user'],
                      password=mysqlcreds['password'],
                      database=mysqlcreds['database'],
                      cursorclass=pymysql.cursors.Cursor)

# Create a SQL query string to get the user data we need from auth_user table
query_users = ('SELECT username AS "uniqname", date_joined, '
               'last_login, is_superuser, is_staff '
               'FROM auth_user;')

# Load the data into a pandas DataFrame
dbusers = pd.read_sql(query_users, conmysql)

# Convert the float 1s and 0s to boolean
dbusers.is_staff = dbusers.is_staff.astype(bool)
dbusers.is_superuser = dbusers.is_superuser.astype(bool)

# Create a SQL query string to get the event data we need from tracking_event table
query_events = ('SELECT e.name, e.timestamp, e.note, u.username '
                'FROM student_explorer.tracking_event e '
                'LEFT JOIN student_explorer.auth_user u '
                'ON e.user_id = u.id;')

events = pd.read_sql(query_events, conmysql)
