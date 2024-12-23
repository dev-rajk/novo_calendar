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

def get_events(status):
    events_ref = db.collection('events').where('status', '==', status)
    events = events_ref.stream()
    quizzes = []
    for event in events:
            event_data = event.to_dict()
            event_data['id'] = event.id
            quizzes.append(event_data)
            
    return quizzes
    

def approve_event(event_id):
    doc_ref = db.collection('events').document(event_id)
    doc_ref.update({'status': 'Approved'})

def decline_event(event_id):
    doc_ref = db.collection('events').document(event_id)
    doc_ref.update({'status': 'Declined'})

def update_event(event_id, quiz_name, date, time, category, venue, location, organizer, genre, quiz_master, prize, contact_number, registration_link, other_details):
    doc_ref = db.collection('events').document(event_id)
    doc_ref.update({
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
        'status': 'Pending'
    })

def delete_event(event_id):
    db.collection('events').document(event_id).delete()

visitor_ref = db.collection("visitor_data").document("counter")

def get_vc():
    """Fetch the current visitor count from Firestore."""
    try:
        doc = visitor_ref.get()
        if doc.exists:
            return doc.to_dict().get("count", 0)
        else:
            # If the document does not exist, create it with initial count of 0
            visitor_ref.set({"count": 0})
            return 0
    except Exception as e:
        print(f"Error getting visitor count: {e}")
        return 0
    
def update_vc(count):
    """Update the visitor count in Firestore."""
    try:
        visitor_ref.update({"count": count})
    except Exception as e:
        print(f"Error updating visitor count: {e}")
