#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import datetime

# Sample DataFrame
data = {
    'mindate': ['2023-01-01 09:00:00', '2023-01-01 14:30:00', '2023-01-02 20:30:00','2023-01-25 19:10:00'],
    'maxdate': ['2023-01-01 11:30:00', '2023-01-01 16:45:00', '2023-01-03 09:45:00','2023-01-28 19:10:00'],
}

df = pd.DataFrame(data)

# Convert date columns to datetime
df['mindate'] = pd.to_datetime(df['mindate'])
df['maxdate'] = pd.to_datetime(df['maxdate'])

# Define the time range to exclude (8 pm to 10 am)
exclude_start_time = pd.to_datetime('20:00:00').time()
exclude_end_time = pd.to_datetime('10:00:00').time()

# Calculate TAT excluding the specified time range
df['TAT_minutes'] = (
    (df['maxdate'] - df['mindate']).dt.total_seconds() / 60 -  # Convert seconds to minutes
    ((df['maxdate'].dt.time >= exclude_start_time) & (df['maxdate'].dt.time < exclude_end_time)) * 60  # Subtract excluded time
)
df['days']=(df['maxdate'] - df['mindate']).dt.days
df['days']=df['days']+1
df['mindateto8pm']=pd.to_datetime(df['mindate'].dt.date) + pd.to_timedelta('20:00:00')
df


# In[30]:


df['mindateto8pm']=pd.to_datetime(df['mindateto8pm'])
import numpy as np
df['mindateto8pm2']=np.where(df['mindateto8pm']>=df['maxdate'],df['maxdate'],df['mindateto8pm'])
df['fistdaymin']=(df['mindateto8pm']-df['mindate']).dt.total_seconds() / 60
df


# In[41]:


from datetime import datetime, timedelta
# Define working hours
working_start_time = datetime.strptime('10:00:00', '%H:%M:%S').time()
working_end_time = datetime.strptime('20:00:00', '%H:%M:%S').time()

# Function to calculate working hours within each day
def calculate_working_hours_per_day(start_time, end_time):
    start_date = start_time.date()
    end_date = end_time.date()

    total_hours = 0
    print("\n1 start_time:",start_time,"<> start_date:",start_date,"\n end_time:",end_time,"<> end_date:",end_date)#######
    # Iterate through each day between start_date and end_date
    current_date = start_date
    while current_date <= end_date:
        # Determine the working hours for the current day
        working_start = max(start_time, datetime.combine(current_date, working_start_time))
        working_end = min(end_time, datetime.combine(current_date, working_end_time))
        daily_hours = max((working_end - working_start).total_seconds() / 3600, 0)
        print("2 working_start",working_start,"<> working_end",working_end,"<> daily_hours",daily_hours)
        
        # Add daily working hours to the total
        total_hours += daily_hours

        # Move to the next day
        current_date += timedelta(days=1)

    return total_hours

# Recalculate TAT for the entire DataFrame considering only working hours within each day
df['TAT_WH'] = df.apply(lambda row: calculate_working_hours_per_day(row['mindate'], row['maxdate']), axis=1)
df
# 16-5-70 m
# 11-4-68 p

