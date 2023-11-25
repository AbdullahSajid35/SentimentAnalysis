import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
import requests
# Page title
st.title("Daily Mood Tracker")

# Date input
selected_date = st.date_input("Select Date", datetime.today())

# Time input with a default time set to noon (12:00 PM)
default_time = datetime.strptime("12:00 PM", "%I:%M %p").time()
selected_time = st.time_input("Select Time", default_time)

data=pd.read_csv('https://raw.githubusercontent.com/AbdullahSajid35/SentimentAnalysis/master/mood_tracker_dataset.csv')
for i in ['hours','minutes']:
    data[i]=data[i].astype('int')
columns=['day', 'hours', 'minutes', 'month_Aug', 'month_Dec', 'month_Feb', 'month_Jan', 'month_Jul',
 'month_Jun', 'month_Mar', 'month_May', 'month_Nov', 'month_Oct', 'month_Sep', 'weekday_Monday', 
 'weekday_Saturday', 'weekday_Sunday', 'weekday_Thursday', 'weekday_Tuesday', 'weekday_Wednesday', 
 'cooking', 'movies', 'holotropic ', 'Dota 2', 'learning ', 'party', 'hiking ', 'love', 'Exercise ',
  'coding ', 'shower', 'meditation ', 'kaballah', 'Email', 'shave ', 'yoga', 'friends', 'repair',
   'Art', 'songs', 'shopping', 'weight log', 'phd', 'podcast', 'reading', 'reddit', 'travel', 
   'research ', 'Recording ', 'trimming ', 'Documentary ', 'penpal', 'walk', 'Watching series ', 
   'Tutorial ', 'good meal', 'Quran ', 'News Update', 'family', 'power nap', 'cleaning', 'writing', 
   'new things ', 'video editing ', 'Write dairy ', 'fasting ', 'prayer', 'Poetry ', 'keto',
    'Audio books ', 'youtube', 'language learning ', 'designing ', 'hospital ', 'streaming ', 'gaming', 
    'jobs']


mapping={0: 'Amazing', 1: 'Awful', 2: 'Bad', 3: 'Good', 4: 'Normal'}
# Multi-selection box for daily activities
activities =['hiking ', 'phd', 'reading', 'writing', 'reddit', 'keto', 'prayer',
 'podcast', 'trimming ', 'Documentary ', 'Quran ', 'new things ', 'gaming', 
 'learning ', 'family', 'News Update', 'Dota 2', 'shower', 'streaming ', 'love',
  'power nap', 'video editing ', 'Watching series ', 'yoga', 'travel', 
  'Write dairy ', 'Exercise ', 'hospital ', 'kaballah', 'Tutorial ',
   'Audio books ', 'walk', 'Poetry ', 'penpal', 'shave ', 'repair', 
   'shopping', 'friends', 'cooking', 'weight log', 'movies', 'meditation ',
    'fasting ', 'Art', 'party', 'Email', 'language learning ', 'good meal', 
    'jobs', 'youtube', 'cleaning', 'holotropic ', 'designing ', 'research ', 
    'coding ', 'Recording ', 'songs']

selected_activities = st.multiselect("Select Daily Activities", activities)
day=selected_date.day
hours=selected_time.hour;
minutes=selected_time.minute
month=selected_date.strftime("%b")
weekday=selected_date.strftime("%A")

df=pd.DataFrame([np.zeros(len(columns),dtype='int')],columns=columns)
df['day']=day
df['hours']=hours
df['minutes']=minutes
if month !='Apr':
    df[f'month_{month}']=1
if weekday!='Friday':
    df[f'weekday_{weekday}']=1
for activity in selected_activities:
    df[activity]=1

for col in df.columns:
    df[col]=df[col].astype('int')
# st.write('Displaying DataFrame: ')
# st.dataframe(df)

url='https://github.com/AbdullahSajid35/SentimentAnalysis/raw/master/mood_tracker_model.pkl'
response=requests.get(url)

if response.status_code==200:
    content=response.content
    model=pickle.loads(content)

label=model.predict([list(df.iloc[0])])[0]
mood=mapping[label]

set_=set()
if mood not in ['Good']:
    df=data[(data['mood']=='Good')&(data['month']==month)&(data['weekday']==weekday)]
    for idx,row in df.iterrows():
        for i in data.loc[idx,'activities'].split(' | '):
            set_.add(i)
activities=[i for i in list(set_) if i not in selected_activities]
if len(activities)>12:
    activities=[list(set_)[i] for i in range(12)]
# Display activities in a styled grid layout
if mood=='Good':
    pharase='You\'re feeling really good today!'
elif mood=='Amazing':
    pharase='You\'re on top of the world!'
elif mood=='Normal':
    pharase='Nothing extraordinary today!'
elif mood=='Awful':
    pharase='Hang in there. Things will get better. You\'re not alone!'
else:
    pharase='I understand it\'s tough right now. You\'re stronger than you think!'
if mood in ['Good','Amazing']:
    st.info(pharase)
else:
    st.error(pharase)
st.markdown("<div ><h2>Check out these activities to lift your spirits</h2></div>", unsafe_allow_html=True)
if len(activities)==0:
    activities=['Quran ','Recording ','Tutorial ','Watching series ','Write dairy ',
    'cleaning','coding ','cooking','designing ','family','fasting ','friends']
# Define CSS style for grid layout
style = """
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 10px;
    justify-items: center; /* Centers items within grid cells */
    justify-content: center; /* Centers the grid horizontally */
    align-items: center; /* Centers the grid vertically */
"""

# Apply HTML and CSS for styling
st.markdown(f'<div style="{style}">' + ''.join(f'<div>{activity}</div>' for activity in activities) + '</div>', unsafe_allow_html=True)
# Format and display selected inputs
# st.write("Day of month:", selected_date.day)
# st.write("Hour:", selected_time.hour) 
# st.write("Minutes:", selected_time.minute)  # Format time in AM/PM
# st.write("Month:", selected_date.strftime("%b"))  # Three-letter month abbreviation
# st.write("Weekday:", selected_date.strftime("%A"))  # Full weekday name

