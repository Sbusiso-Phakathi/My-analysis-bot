#!/usr/bin/env python3

import streamlit as st
import cv2
import face_recognition
import time
import gspread
from google.oauth2.service_account import Credentials
import datetime
import pandas as pd
import requests
import numpy as np
from PIL import Image
import io, os

# Streamlit App Title
st.title("Face Recognition Time Logger")

# Get username from environment
username = os.environ.get('USER')
image_url = f"https://github.com/Sbusiso-Phakathi/recruit/blob/main/{username}.jpg?raw=true"
status_placeholder = st.empty()

# Load the known image
response = requests.get(image_url)
if response.status_code == 200:
    image = Image.open(io.BytesIO(response.content))
    
    if image.mode == "RGBA":
        image = image.convert("RGB")
    
    known_image = np.array(image)

    image_placeholder = st.empty()

else:
    status_placeholder.error("Error: Could not load the image.")
    st.stop()

# Google Sheets authorization
credentials = Credentials.from_service_account_file(f"/Users/{username}/Desktop/face/automatic-time-379113-5440df4089b9.json")
scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
gc = gspread.authorize(scoped_credentials)


with st.spinner("Fetching learner data..."):
    all_learners = gc.open("all_learners")
    worksheet = all_learners.worksheet('Sheet1')
    df = pd.DataFrame(worksheet.get_all_values(), columns=['Username', 'First Name', 'Last Name', 'Employee Number', 'Cohort'])

status_placeholder.success("Learner data fetched successfully!")
# Fetch learner data from Google Sheets
# st.write("Fetching learner data...")
# all_learners = gc.open("all_learners")
# worksheet = all_learners.worksheet('Sheet1')
# df = pd.DataFrame(worksheet.get_all_values(), columns=['Username', 'First Name', 'Last Name', 'Employee Number', 'Cohort'])

# Extract learner information
firstname = df.loc[df['Username'] == username, 'First Name'].values[0]
lastname = df.loc[df['Username'] == username, 'Last Name'].values[0]
empno = df.loc[df['Username'] == username, 'Employee Number'].values[0]
cohort = df.loc[df['Username'] == username, 'Cohort'].values[0]

# Access cohort sheet
sh = gc.open(cohort).sheet1
dx = pd.DataFrame(sh.get_all_values(), columns=['Date', 'First Name', 'Last Name', 'Employee Number'])

# Check attendance dates
date = dx.loc[dx['First Name'] == firstname, 'Date'].values
days = [datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S').day for dt_str in date]
day_ = datetime.datetime.now().day

# Encode the known face
known_encoding = face_recognition.face_encodings(known_image)[0]

# If today's date is not in the attendance list, prompt for face capture
if day_ not in days:
    
    if 1 == 1:
        # Start webcam
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            status_placeholder.error("Error: Could not open webcam.")
        else:
            # Create a placeholder for the video feed

            # Store match state in session state
            if 'matched' not in st.session_state:
                st.session_state.matched = False

            while not st.session_state.matched:
                ret, frame = video_capture.read()
                if ret:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Update the image in the placeholder
                    image_placeholder.image(rgb_frame, caption="Live video feed", use_column_width=True)

                    unknown_encodings = face_recognition.face_encodings(rgb_frame)

                    if unknown_encodings:
                        unknown_encoding = unknown_encodings[0]
                        
                        results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.45)
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        if results[0]:
                            st.session_state.matched = True
                            status_placeholder.success("Match found!")
                            sh.append_row([current_time, firstname, lastname, empno])
                            st.write(f"Logged entry for {firstname} {lastname} at {current_time}")

                            break
                        else:
                            status_placeholder.warning("No match found. Scanning again...")
                    else:
                        status_placeholder.warning("No faces found in the captured frame.")

                # Small delay to avoid overwhelming the CPU
                time.sleep(0.1)

            # Release the webcam
            video_capture.release()
else:
    st.write(f"{firstname} {lastname} already logged attendance today.")
