import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import pandas as pd

# Initialize Firestore using secrets
if not firebase_admin._apps:  # Check if the app is already initialized
    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Firestore operations
def add_event(quiz_name, date, time, category, venue, location, organizer, genre, quiz_master, prize, contact_number, registration_link, other_details):
    doc_ref = db.collection('events').document()
    doc_ref.set({
        'quiz_name': quiz_name,
        'date': str(date),
        'time': time,
        'category': category,
        'venue': venue,
        'location': location,
        'organizer': organizer,
        'genre': genre,
        'quiz_master': quiz_master,
        'prize': prize,
        'contact_number': contact_number,
        'registration_link': str(registration_link),
        'other_details': other_details,
        'status': 'Approved'
    })

def get_events_dated(curr_dt):
    events_ref = db.collection("events").where("date", ">", curr_dt)

    events = events_ref.stream()
    quizzes = []
    for event in events:
            event_data = event.to_dict()
            event_data['id'] = event.id
            quizzes.append(event_data)
            
    return quizzes
    

