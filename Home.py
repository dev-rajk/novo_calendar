import streamlit as st
from db import add_event, get_events, approve_event, update_event, delete_event, decline_event, get_vc, update_vc
import pandas as pd
import json


st.set_page_config(
    page_title="Assam Quiz Calendar",
    layout="wide", 
    page_icon=":material/lightbulb:",
    menu_items={
        'about': '''**This was made with love in Assam**        
        The calendar attempts to help organisers and participants know more about the quizzing events across the state. 
        
        '''}
    )
# st.page_link("Home.py", label="Home", icon=":material/lightbulb:")
# st.page_link("pages/admin_page.py", label="Submit Events", icon=":material/lightbulb:")
# st.page_link("pages/submit_page.py", label="Manage Events", icon=":material/lightbulb:")



# Check if 'has_visited_homepage' exists in session_state
if 'has_visited_homepage' not in st.session_state:
        # If not, this is the user's first time visiting the homepage in this session
        st.session_state.has_visited_homepage = False

    # If this is the first time loading the homepage, update the visitor count
if not st.session_state.has_visited_homepage:
        # Get the current visitor count from Firestore
        count = get_vc()

        # Increment the visitor count
        count += 1

        # Update the visitor count in Firestore
        update_vc(count)

        # Set the flag in session_state to prevent further updates during the session
        st.session_state.has_visited_homepage = True

st.title("Assam Quiz Calendar :calendar: ")
st.write('Select in sidebar to view quizzes or submit events')

# FullCalendar HTML and JavaScript with custom modal including all event details
def fullcalendar(events, theme_mode):
    events_json = json.dumps(events)  # Convert events to JSON string
    
    # Styles for light and dark mode
    light_style = """
    body {
        background-color: white;
        color: black;
        font-family: Arial, sans-serif;
    }
    .modal-content {
        background-color: white;
        color: black;
        font-family: Arial, sans-serif;
    }
    .fc-event, .fc-daygrid-event, .fc-daygrid-event-dot {
        color: black;
        background-color: teal;
    }
    """
    
    dark_style = """
    body {
        background-color: black;
        color: black;
        font-family: Arial, sans-serif;
    }
    .modal-content {
        background-color: #2e2e2e;
        color: white;
        font-family: Arial, sans-serif;
    }
    .fc-event, .fc-daygrid-event, .fc-daygrid-event-dot {
        color: black;
        background-color: teal;
    }
    """

    # Determine the style based on the theme mode
    selected_style = dark_style if theme_mode == 'dark' else light_style

    calendar_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.css' rel='stylesheet' />
        <script src='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js'></script>
        <style>
            /* The Modal (background) */
            .modal {{
                display: none; /* Hidden by default */
                position: fixed; /* Stay in place */
                z-index: 1; /* Sit on top */
                left: 0;
                top: 0;
                width: 100%; /* Full width */
                height: 100%; /* Full height */
                overflow: auto; /* Enable scroll if needed */
                background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
                padding-top: 60px;
            }}

            /* Modal Content */
            .modal-content {{
                background-color: #fefefe;
                margin: 5% auto; /* 15% from the top and centered */
                padding: 20px;
                border: 1px solid #888;
                width: 80%; /* Could be more or less, depending on screen size */
            }}

            /* The Close Button */
            .close {{
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }}

            .close:hover,
            .close:focus {{
                color: black;
                text-decoration: none;
                cursor: pointer;
            }}

            /* Dynamic Style based on theme */
            {selected_style}
        </style>
        <script>
          document.addEventListener('DOMContentLoaded', function() {{
            var calendarEl = document.getElementById('calendar');
            var modal = document.getElementById('myModal');
            var closeModal = document.getElementsByClassName('close')[0];

            // Close the modal when the user clicks on <span> (x)
            closeModal.onclick = function() {{
                modal.style.display = "none";
            }}

            // Close the modal when the user clicks outside of it
            window.onclick = function(event) {{
                if (event.target == modal) {{
                    modal.style.display = "none";
                }}
            }}

            var calendar = new FullCalendar.Calendar(calendarEl, {{
              initialView: 'dayGridMonth',  // Default to month view
              headerToolbar: {{
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek'  // Toggle between month and week views
              }},
              events: {events_json},
              eventClick: function(info) {{
                // Populate modal with all event details
                document.getElementById('modal-title').innerText = info.event.title;
                document.getElementById('modal-date').innerText = info.event.start.toLocaleDateString();
                document.getElementById('modal-time').innerText = info.event.extendedProps.time || 'N/A';
                document.getElementById('modal-venue').innerText = info.event.extendedProps.venue || 'N/A';
                document.getElementById('modal-location').innerText = info.event.extendedProps.location || 'N/A';
                document.getElementById('modal-organizer').innerText = info.event.extendedProps.organizer || 'N/A';
                document.getElementById('modal-category').innerText = info.event.extendedProps.category || 'N/A';
                document.getElementById('modal-quiz-master').innerText = info.event.extendedProps.quiz_master || 'N/A';
                document.getElementById('modal-genre').innerText = info.event.extendedProps.genre || 'N/A';
                document.getElementById('modal-prize').innerText = info.event.extendedProps.prize || 'N/A';
                document.getElementById('modal-contact').innerText = info.event.extendedProps.contact_number || 'N/A';
                document.getElementById('modal-registration_link').innerHTML = info.event.extendedProps.registration_link || 'N/A';
                document.getElementById('modal-other_details').innerText = info.event.extendedProps.other_details || 'N/A';

                // Display the modal
                modal.style.display = "block";
              }}
            }});
            calendar.render();
          }});
        </script>
    </head>
    <body>

        <!-- FullCalendar -->
        <div id='calendar'></div>

        <!-- The Modal -->
        <div id="myModal" class="modal">
          <div class="modal-content">
            <span class="close">&times;</span>
            <h2 id="modal-title"></h2>
            <p><strong>Date:</strong> <span id="modal-date"></span></p>
            <p><strong>Time:</strong> <span id="modal-time"></span></p>
            <p><strong>Venue:</strong> <span id="modal-venue"></span></p>
            <p><strong>Location:</strong> <span id="modal-location"></span></p>
            <p><strong>Organizer:</strong> <span id="modal-organizer"></span></p>
            <p><strong>Category:</strong> <span id="modal-category"></span></p>
            <p><strong>Quiz Master:</strong> <span id="modal-quiz-master"></span></p>
            <p><strong>Genre:</strong> <span id="modal-genre"></span></p>
            <p><strong>Prize:</strong> <span id="modal-prize"></span></p>
            <p><strong>Contact Number:</strong> <span id="modal-contact"></span></p>
            <p><strong>Registration Link (External link! Be Careful!! Copy to another tab):</strong> <span id="modal-registration_link"></span></p>
            <p><strong>Other Details:</strong> <span id="modal-other_details"></span></p>
          </div>
        </div>

    </body>
    </html>
    """
    return calendar_code

def link_string(link_str):
    if link_str.startswith('http'):
        return str(f'{link_str }')
    else:
        y = 'https://'
        return str(f'{y}{link_str }')
# def link_string(link_str):
#     if link_str.startswith('http'):
#         return str(f'<a href="{link_str }" target="_blank" rel="external">Click here to go to external link </a>')
#     else:
#         y = 'https://'
#         return str(f'<a href="{y}{link_str }" target="_blank" rel="external">Click here to go to external link </a>')



# 1. Viewing Events

st.subheader("Upcoming Quizzes")
approved_events = get_events("Approved")
    
if approved_events:
        # Prepare events for FullCalendar
        events = []
        for event in approved_events:
            events.append({
            "title": event['quiz_name'],  # Quiz Name
            "start": event['date'],  # Date
            "extendedProps": {  # Additional event details
            "time": event['time'], 
                        "category": event['category'],  # Venue (renamed from place)
                        "venue": event['venue'],
                        "location":   event['location'], # Location
                        "organizer": event['organizer'],                    
                        "genre": event['genre'],
                        "quiz_master": event['quiz_master'],  # Quiz Master
                        "prize": event['prize'],
                        "contact_number": event['contact_number'],  # Contact Number
                        "registration_link": link_string(event["registration_link"]),
                        "other_details": event['other_details']
                    }
                })
            
        # Retrieve current theme mode from Streamlit settings
        theme_mode = st.get_option('theme.base')  # 'light' or 'dark'

        # Display FullCalendar with modal functionality based on the global theme
        st.components.v1.html(fullcalendar(events, theme_mode=theme_mode), height=800)

        st.write('''
                :red[**This website is free of cost for all users.** ] \n
                :red[**The maintainers bear no responsibility for the accuracy of the event information, or any loss or damages resulting from the use of this site. The maintainer is not liable for any damages or misinformation.**] \n
                :red[**Users are encouraged to verify all event information.**] \n
                :red[**No personal infomation is tracked.**] \n
                :green[**Cheers to quizzing.** ] :partying_face::partying_face:\n
                  ''')

            
else:
        st.write("No approved events to show.")
        st.write('''
                :red[ **This website is free of cost for all users.** ] \n
                :red[**The maintainers bear no responsibility for the accuracy of the event information, or any loss or damages resulting from the use of this site. The maintainer is not liable for any damages or misinformation.** ]  \n
                :red[**Users are encouraged to verify all event information.**] \n
                :red[**No personal infomation is tracked.** ] \n
                :green[**Cheers to quizzing.** ] :partying_face::partying_face:\n
                  ''')

# Display the current visitor count
current_count = get_vc()  # Get the latest count from Firestore
st.write(f"Number of visitors: {current_count}")
