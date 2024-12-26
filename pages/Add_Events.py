import streamlit as st
from db import add_event, get_events, approve_event, update_event, delete_event, decline_event
st.set_page_config(
    page_title="Contribute: Submit Events",
    layout="centered", 
    page_icon=":material/lightbulb:",
    menu_items={
        'about': '''**This was made with love in Assam**        
        The calendar attempts to help organisers and participants know more about the quizzing events across the state. 
        
        '''}
    )
st.title("Assam Quiz Calendar :calendar: ")
st.subheader("Submit a New Quiz Event")
    
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
        
        submit_button = st.form_submit_button(label='Add Event')
        
        if submit_button:
            if not Title or not Contact or not Location or not Date or not Category or not Time:
                st.error("Please fill all the fields marked with a *")
            else:
                add_event(Title, Date, Time, Category, Venue, Location, Organizer, Genre, Quiz_Master, Prize, Contact, registration_link, other_details)
                st.success(f"Event '{Title}' added successfully!")
                # st.success(f"Event '{Title}' submitted successfully! Awaiting admin approval.")

st.markdown('''
                :red[ **This website is free of cost for all users.** ] \n
                :red[**The maintainers bear no responsibility for the accuracy of the event information, or any loss or damages resulting from the use of this site. The maintainer is not liable for any damages or misinformation.** ]  \n
                :red[**Users are encouraged to verify all event information.** ] \n
                :red[**No personal infomation is tracked.** ] \n
                :red[**Cheers to quizzing.** ] :partying_face::partying_face:\n
                  ''')
