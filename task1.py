import threading
import cv2
import face_recognition
import sqlite3
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from datetime import datetime

import task1
import Port
class Task1():
    database_file = r"C:\Users\long0\PycharmProjects\Project_Intro_toCS\face_encodings.db"

    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        # Initialize variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.sent_names = set()  # Keep track of names that have been sent
        self.video_capture = cv2.VideoCapture(0)

        # Connect to the SQLite database
        self.conn = sqlite3.connect(self.database_file)
        self.cursor = self.conn.cursor()

        # Load the face encodings from the database
        self.cursor.execute("SELECT encoding, name FROM face_encodings")
        self.rows = self.cursor.fetchall()


    def Task1_process(self):
        for row in self.rows:
            encoding_bytes = row[0]
            name = row[1]
            encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
            encoding = encoding.reshape((128,))  # Resize the encoding to match face_recognition
            self.known_encodings.append(encoding)
            self.known_names.append(name)

    def Task1_face_detection(self):
        self.Task1_process()
        while True:
            # Capture video frame-by-frame
            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()

            # Resize frame to speed up face recognition
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (OpenCV default) to RGB color
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and their encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            count = 0
            for face_encoding in face_encodings:
                # Compare the face encoding with known encodings
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    # Find the indices of all matched faces
                    matched_indices = [i for i, match in enumerate(matches) if match]

                    # Select the first matched face and retrieve the corresponding name
                    first_match_index = matched_indices[0]
                    name = self.known_names[first_match_index]
                self.face_names.append(name)
                # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back the face locations and draw rectangle and name
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)

                # Display the resulting image
            cv2.imshow("Video", frame)

            # Exit the loop if 'q' is pressed

            # Release the video capture and close all windows
            self.video_capture.release()
            if self.face_names == ["Unknown"]:
                print("Invalid, try again...")
                continue
            if self.face_names == ["Long"] or self.face_names == ["MinhAnh"] or self.face_names == ["Tommy"]:
                Port.sendCommand("1")
                time.sleep(2)
                Port.sendCommand("0")
                print("Checking completed!")
                print("Valid Face!")
                time.sleep(1)
                cv2.destroyAllWindows()
                break


task1 = Task1()
task1.Task1_face_detection()

