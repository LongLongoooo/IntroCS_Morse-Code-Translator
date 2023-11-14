import os
import cv2
import face_recognition
import sqlite3
import numpy as np
print("Hello AI")
# Connect to the SQLite database or create a new one
conn = sqlite3.connect(r"\Users\long0\PycharmProjects\Project_Intro_toCS\face_encodings.db")
cursor = conn.cursor()

# Create a table to store the face encodings and image names
cursor.execute("CREATE TABLE IF NOT EXISTS face_encodings (id INTEGER PRIMARY KEY, encoding BLOB, name TEXT)")

# Specify the root folder path containing the image files
root_folder = r"C:\Users\long0\PycharmProjects\Project_Intro_toCS\Train_photos"

def extract_name_from_filename(filename):
    print("Processing 1....")
    # Split the filename by "_" to extract the name
    parts = filename.split(" ")
    if len(parts) >= 1:
        return parts[0]
    else:
        return "Unknown"

def process_images(folder_path):
    print("Processing 2....")
    for root, dirs, files in os.walk(folder_path):
        # Iterate over the files in the current folder
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                # Convert the image from BGR to RGB
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Find faces in the image
                face_locations = face_recognition.face_locations(rgb_image)
                face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

                # Extract the name from the filename
                name = extract_name_from_filename(file)
                print(name)

                # Check if the image file already exists in the database
                cursor.execute("SELECT name FROM face_encodings WHERE name=?", (name,))
                existing_files = cursor.fetchall()
                if not existing_files:
                    # Insert the face encodings and image name into the database
                    for encoding in face_encodings:
                        cursor.execute("INSERT INTO face_encodings (encoding, name) VALUES (?, ?)", (encoding.tobytes(), name))

        # Commit the changes after processing all images in the current folder
        conn.commit()

# Process images in the root folder and its subfolders
process_images(root_folder)

# Close the database connection
conn.close()
