import streamlit as st
from datetime import datetime
from db import add_event, get_events_dated
import pandas as pd
st.set_page_config(
    page_title="Assam Quiz Calendar",
    layout="wide", 
    page_icon=":material/lightbulb:",
    menu_items={
        'about': '''**This was made with love in Assam**        
        The calendar attempts to help organisers and participants know more about the quizzing events across the state. 
        A small tribute to Arindam, taken from us far too soon
        '''}
    )

st.title("Assam Quiz Calendar :calendar: ")
st.write('''Curated by Rajibul Awal :sunglasses: Dipom Saha :turtle: and Devraj Kashyap :clown_face:''')
st.write("Find upcoming events or add your own events")


upcoming_events = get_events_dated(str(datetime.now().date()), ['Approved', 'Pending'])

df = pd.DataFrame(upcoming_events, columns= ['quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details' ])

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
df['date'] = df['date'].dt.date

df = df.sort_values(by='date')

df['date'] = df['date'].apply(lambda x: x.strftime('%d %b, %Y'))

df_reset = df[['quiz_name', 'date', 'time', 'category', 'venue', 'location', 'prize', 'contact_number', 'organizer', 'genre', 'quiz_master', 'registration_link', 'other_details']].reset_index(drop=True)


df_reset['registration_link'] = df_reset['registration_link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) else '')

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
df_reset.insert(0, 'Sl. No.', range(1, len(df_reset) + 1))

fest_contacts = df_reset['Contact Number'].value_counts()
fest_contacts = fest_contacts[fest_contacts > 1].index.tolist()

highlight_palette = [
    '#f9f6e9',  # soft yellow
    '#e9f6f9',  # soft blue
    '#f6e9f9',  # soft pink
    '#e9f9f0',  # soft green
    '#fff4e6',  # warm peach
    '#fef9e7',  # lemon tint
    '#f4f4f4',  # light grey
]

fest_color_map = {
    contact: highlight_palette[i % len(highlight_palette)]
    for i, contact in enumerate(fest_contacts)
}

df_reset['highlight_color'] = df_reset['Contact Number'].apply(lambda x: fest_color_map.get(x, ''))

def styled_row(row):
    style = f'background-color:{row["highlight_color"]};' if row['highlight_color'] else ''
    row_html = f'<tr style="{style}">'
    for col in df_reset.columns[:-1]:  # exclude 'highlight_color'
        row_html += f'<td>{row[col]}</td>'
    row_html += '</tr>'
    return row_html

table_headers = ''.join(f'<th>{col}</th>' for col in df_reset.columns[:-1])
table_rows = '\n'.join(df_reset.apply(styled_row, axis=1))
table_html = f'''
<table>
<thead><tr>{table_headers}</tr></thead>
<tbody>{table_rows}</tbody>
</table>
'''

st.markdown(table_html, unsafe_allow_html=True)

st.subheader("Submit an Upcoming Quiz ")
with st.form(key='event_form', clear_on_submit=True):
        st.write(''':red[Please ensure that event details are accurate] ''') 
        st.write(''':red[Fields marked with * are necessary]''')
        Title = st.text_input("Quiz Name*")
        Date = st.date_input("Date*")
        Time = st.text_input("Time*")
        Category = st.text_input("Category*")
        Venue = st.text_input("Venue")  
        Location = st.text_input("Location*")
        Organizer = st.text_input("Organizer")
        Genre = st.text_input("Genre")
        Quiz_Master = st.text_input("Quiz Master")
        Prize = st.text_input("Prize")
        Contact = st.text_input("Contact Number*")
        registration_link = st.text_input(" Registration Link")
        other_details = st.text_area("Other Details")
        
        submit_button = st.form_submit_button(label='Submit Event')
        
        if submit_button:
            if not Title or not Contact or not Location or not Date or not Category or not Time:
                st.error("Please fill all the fields marked with a *")
            else:
                add_event(Title, Date, Time, Category, Venue, Location, Organizer, Genre, Quiz_Master, Prize, Contact, registration_link, other_details)
                st.success(f"Event '{Title}' added!!!")
st.write('''
                :red[**DISCLAIMER**] \n
                :red[**This website is free of cost for all users.** ] \n
                :red[**Users are encouraged to verify all event information.**] \n
                :red[**No personal infomation is tracked.**] \n
                :green[**Cheers to quizzing.** ] :partying_face: :partying_face:\n
                  ''')
