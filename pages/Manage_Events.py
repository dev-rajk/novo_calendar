import streamlit as st
from db import add_event, get_events, approve_event, update_event, delete_event, decline_event
import pandas as pd
st.set_page_config(
    page_title="Admin: Manage Events",
    layout="centered", 
    page_icon=":material/lightbulb:",
    menu_items={
        'about': '''**This was made with love in Assam**        
        The calendar attempts to help organisers and participants know more about the quizzing events across the state. 
        
        '''}
    )
st.title("Assam Quiz Calendar :calendar: ")
st.subheader("Admin: Manage Events")
BASIC_ADMIN_PASSWORD = st.secrets.user.pass1
FULL_ADMIN_PASSWORD = st.secrets.user.pass2

password = st.text_input("Enter Admin Password", type="password")

if password == BASIC_ADMIN_PASSWORD:
        # Fetch events based on status
        approved_events = get_events("Approved")
        pending_events = get_events("Pending")
        declined_events = get_events("Declined")
    
        # Tab to switch between managing approved and pending events
        tab1, tab2, tab3 = st.tabs(["Manage Approved Events", "Approve Pending Events", "Declined Events"])
    
        with tab1:  # Manage Approved Events Tab
            st.write("Manage Approved Events")
            
            if  approved_events:
                
                df = pd.DataFrame(approved_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"], key =1)
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form_accepted_1'):
                    Title = st.text_input("Quiz Name", value=selected_event["quiz_name"])
                    Date = st.date_input("Date", value=pd.to_datetime(selected_event["date"]))
                    Time = st.text_input("Time", value=selected_event["time"])
                    Category = st.text_input("Category", value=selected_event["category"])
                    Venue = st.text_input("Venue", value=selected_event["venue"])
                    Location = st.text_input("Location", value=selected_event["location"])
                    Organizer = st.text_input("Organizer", value=selected_event["organizer"])
                    Genre = st.text_input("Genre", value=selected_event["genre"])
                    Quiz_Master = st.text_input("Quiz Master", value=selected_event["quiz_master"])
                    Prize = st.text_input("Prize", value=selected_event["prize"])
                    Contact = st.text_input("Contact Number", value=selected_event["contact_number"])
                    registration_link = st.text_input(" Registration Link", value=selected_event["registration_link"])
                    other_details = st.text_area("Other Details", value=selected_event["other_details"])
        
    
                    submit_button = st.form_submit_button(label='Update Event')
                    st.write('Updated events need to be approved again')
                   
    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, Quiz_Master, Prize, Contact, registration_link, other_details)
                        st.success(f"Event ID {selected_event_id} updated successfully!")
    
                # Button to export approved events as a CSV file
                if st.button('Export Approved Events as CSV'):
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name='approved_events.csv',
                        mime='text/csv',
                    )
    
            else:
                st.markdown("No approved events to manage. :smiley: :smiley: :smiley:")
    
        with tab2:  # Approve Pending Events Tab
            st.write("Approve Pending Events")
    
            if  pending_events:
                
                df_pending = pd.DataFrame(pending_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
                
                st.dataframe(df_pending.drop(columns=["status"]))
    
                selected_event_id_pending = st.selectbox("Select an Event to Approve", df_pending["id"], key =2)
                if st.button("Approve Event"):
                    approve_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} approved!")
                elif st.button("Decline Event"):
                    decline_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} Declined!")
            else:
                st.markdown("No pending events to approve. :smiley: :smiley: :smiley:")
        with tab3:  # Manage Approved Events Tab
            st.write("Manage Declined Events")
            
            if  declined_events:
                
                df = pd.DataFrame(declined_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"], key =3)
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form_declined_1'):
                    Title = st.text_input("Quiz Name", value=selected_event["quiz_name"])
                    Date = st.date_input("Date", value=pd.to_datetime(selected_event["date"]))
                    Time = st.text_input("Time", value=selected_event["time"])
                    Category = st.text_input("Category", value=selected_event["category"])
                    Venue = st.text_input("Venue", value=selected_event["venue"])
                    Location = st.text_input("Location", value=selected_event["location"])
                    Organizer = st.text_input("Organizer", value=selected_event["organizer"])
                    Genre = st.text_input("Genre", value=selected_event["genre"])
                    Quiz_Master = st.text_input("Quiz Master", value=selected_event["quiz_master"])
                    Prize = st.text_input("Prize", value=selected_event["prize"])
                    Contact = st.text_input("Contact Number", value=selected_event["contact_number"])
                    registration_link = st.text_input(" Registration Link", value=selected_event["registration_link"])
                    other_details = st.text_area("Other Details", value=selected_event["other_details"])
        
    
                    submit_button = st.form_submit_button(label='Update Event')
                    st.write('Updated events need to be approved again')
                    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, Quiz_Master, Prize, Contact, registration_link, other_details)
                        st.success(f"Event ID {selected_event_id} updated successfully!")
    
            else:
                st.write("No Declined events.")
elif password == FULL_ADMIN_PASSWORD:
        st.write("Full Admin Mode")
        # Fetch events based on status
        approved_events = get_events("Approved")
        pending_events = get_events("Pending")
        declined_events = get_events("Declined")
        # Tab to switch between managing approved and pending events
        tab1, tab2, tab3 = st.tabs(["Manage Approved Events", "Approve Pending Events", "Declined Events"])
    
        with tab1:  # Manage Approved Events Tab
            st.write("Manage Approved Events")
            
            if  approved_events:
                
                df = pd.DataFrame(approved_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"], key =4)
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form_accepted_2'):
                    Title = st.text_input("Quiz Name", value=selected_event["quiz_name"])
                    Date = st.date_input("Date", value=pd.to_datetime(selected_event["date"]))
                    Time = st.text_input("Time", value=selected_event["time"])
                    Category = st.text_input("Category", value=selected_event["category"])
                    Venue = st.text_input("Venue", value=selected_event["venue"])
                    Location = st.text_input("Location", value=selected_event["location"])
                    Organizer = st.text_input("Organizer", value=selected_event["organizer"])
                    Genre = st.text_input("Genre", value=selected_event["genre"])
                    Quiz_Master = st.text_input("Quiz Master", value=selected_event["quiz_master"])
                    Prize = st.text_input("Prize", value=selected_event["prize"])
                    Contact = st.text_input("Contact Number", value=selected_event["contact_number"])
                    registration_link = st.text_input(" Registration Link", value=selected_event["registration_link"])
                    other_details = st.text_area("Other Details", value=selected_event["other_details"])
        
    
                    submit_button = st.form_submit_button(label='Update Event')
                    st.write('Updated events need to be approved again')
                    delete_button = st.form_submit_button(label='Delete Event')
    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, Quiz_Master, Prize, Contact, registration_link, other_details)
                        st.success(f"Event ID {selected_event_id} updated successfully!")
    
                    if delete_button:
                        # Delete event from the database
                        delete_event(selected_event_id)
                        st.success(f"Event ID {selected_event_id} deleted successfully!")
    
                # Button to export approved events as a CSV file
                if st.button('Export Approved Events as CSV'):
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name='approved_events.csv',
                        mime='text/csv',
                    )
    
            else:
                st.write("No approved events to manage.")
    
        with tab2:  # Approve Pending Events Tab
            st.write("Approve Pending Events")
    
            if  pending_events:
                
                df_pending = pd.DataFrame(pending_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
                
                st.dataframe(df_pending.drop(columns=["status"]))
    
                selected_event_id_pending = st.selectbox("Select an Event to Approve", df_pending["id"], key = 5)
                if st.button("Approve Event"):
                    approve_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} approved!")
                elif st.button("Decline Event"):
                    decline_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} Declined!")
            else:
                st.write("No pending events to approve.")
        with tab3:  # Manage Approved Events Tab
            st.write("Manage Declined Events")
            
            if  declined_events:
                
                df = pd.DataFrame(declined_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"], key =6)
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form_declined_2'):
                    Title = st.text_input("Quiz Name", value=selected_event["quiz_name"])
                    Date = st.date_input("Date", value=pd.to_datetime(selected_event["date"]))
                    Time = st.text_input("Time", value=selected_event["time"])
                    Category = st.text_input("Category", value=selected_event["category"])
                    Venue = st.text_input("Venue", value=selected_event["venue"])
                    Location = st.text_input("Location", value=selected_event["location"])
                    Organizer = st.text_input("Organizer", value=selected_event["organizer"])
                    Genre = st.text_input("Genre", value=selected_event["genre"])
                    Quiz_Master = st.text_input("Quiz Master", value=selected_event["quiz_master"])
                    Prize = st.text_input("Prize", value=selected_event["prize"])
                    Contact = st.text_input("Contact Number", value=selected_event["contact_number"])
                    registration_link = st.text_input(" Registration Link", value=selected_event["registration_link"])
                    other_details = st.text_area("Other Details", value=selected_event["other_details"])
        
    
                    submit_button = st.form_submit_button(label='Update Event')
                    st.write('Updated events need to be approved again')
                    delete_button = st.form_submit_button(label='Delete Event')
    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, Quiz_Master, Prize, Contact, registration_link, other_details)
                        st.success(f"Event ID {selected_event_id} updated successfully!")
    
                    if delete_button:
                        # Delete event from the database
                        delete_event(selected_event_id)
                        st.success(f"Event ID {selected_event_id} deleted successfully!")
            else:
                st.write("No Declined events.")
    
     
elif password:
        st.error("Incorrect Admin Password")

