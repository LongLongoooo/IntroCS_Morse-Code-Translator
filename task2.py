import time
import cv2
import numpy as np
from keras.models import load_model
import Port
import task2_morse

class Task2:
    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)
    cameraID = 0
    def __init__(self):
        print("")
        np.set_printoptions(suppress=True)
        # Load the model
        self.model = load_model("C:\\Users\\long0\\PycharmProjects\\Project_Intro_toCS\\converted_4\\keras_model.h5", compile=False)

        # Load the labels
        self.class_names = open("C:\\Users\\long0\\PycharmProjects\\Project_Intro_toCS\\converted_4\\labels.txt", "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        return

    def Feelings_Detector_Run(self):
        print("Auto mode is activated!!!!")
        while True:
            time.sleep(2)
            # Grab the webcamera's image.
            ret, image = self.camera.read()

            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            # Show the image in a window
            cv2.imshow("Detection Webcam", image)

            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            resized_image = (image / 127.5) - 1

            # Predicts the model
            prediction = self.model.predict(image)
            index = np.argmax(prediction)
            class_name = self.class_names[index]
            confidence_score = prediction[0][index]
            # Print prediction and confidence score
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            print(confidence_score)

            # Make the window respond
            key = cv2.waitKey(1)
            if class_name[2:] == "OVER\n" and confidence_score >= 0.5:
                print("Translating...")
                time.sleep(2)
                task2_morse.OVER()
                continue
            elif class_name[2:] == "HELLO\n" and confidence_score >= 0.9:
                print("Translating...")
                time.sleep(2)
                task2_morse.Hello()
                continue
            elif class_name[2:] == "S.O.S\n" and confidence_score >= 0.2:
                print("Translating...")
                time.sleep(2)
                task2_morse.S_O_S()
                continue

task2 = Task2()
task2.Feelings_Detector_Run()

