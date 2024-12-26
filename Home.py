import streamlit as st
from datetime import datetime
from db import get_events
import pandas as pd
st.set_page_config(
    page_title="Assam Quiz Calendar",
    layout="wide", 
    page_icon=":material/lightbulb:",
    menu_items={
        'about': '''**This was made with love in Assam**        
        The calendar attempts to help organisers and participants know more about the quizzing events across the state. 
        
        '''}
    )
# Title of the Streamlit app
st.title("Assam Quiz Calendar :calendar: ")
st.write('Select in sidebar to view quizzes or submit events')

# Fetch approved events (assuming get_events fetches a list of events)
approved_events = get_events("Approved")
# Convert the list of events into a DataFrame (assuming approved_events is a list of dictionaries)
df = pd.DataFrame(approved_events, columns= ['quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details' ])
    
# Check if the DataFrame has the necessary columns: 'event_name' and 'event_date' (adjust as needed)

# Convert event_date from string to datetime (in the format 'YYYY-MM-DD')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
df['date'] = df['date'].dt.date

# Filter the DataFrame to include only future events
df = df[df['date'] > datetime.now().date()]

# Sort the events by the 'date'
df = df.sort_values(by='date')

# Reset index to remove the index column when displaying the table
df_reset = df[['quiz_name', 'date', 'time', 'category', 'venue', 'location', 'prize', 'contact_number', 'organizer', 'genre', 'quiz_master', 'registration_link', 'other_details']].reset_index(drop=True)

# Make the 'registration_link' column clickable
df_reset['registration_link'] = df_reset['registration_link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) else '')
# Rename columns to something more user-friendly
df_reset = df_reset.rename(columns={
    'quiz_name': 'Quiz Name',
    'date': 'Date',
    'time': 'Time',
    'category': 'Category',
    'venue': 'Venue',
    'location': 'Location',
    'organizer': 'Organizer',
    'genre': 'Genre',
    'quiz_master': 'Quiz Master',
    'prize': 'Prize',
    'contact_number': 'Contact Number',
    'registration_link': 'Registration Link',
    'other_details': 'Other Details'
})
# Display the table with clickable links
st.markdown(df_reset.to_html(escape=False), unsafe_allow_html=True)


st.write('''
                :red[**This website is free of cost for all users.** ] \n
                :red[**The maintainers bear no responsibility for the accuracy of the event information, or any loss or damages resulting from the use of this site. The maintainer is not liable for any damages or misinformation.**] \n
                :red[**Users are encouraged to verify all event information.**] \n
                :red[**No personal infomation is tracked.**] \n
                :green[**Cheers to quizzing.** ] :partying_face::partying_face:\n
                  ''')
