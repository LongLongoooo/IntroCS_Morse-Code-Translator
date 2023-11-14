print("Intelligent-Morse Translator")
print("Check Valid Face...")
import cv2
from task1 import Task1
import time
import scheduler
sche = scheduler.Scheduler()
print("")
sche.SCH_Add_Task(Task1, 5, 5)
print("Welcome user, please enter your option to use the device")
print("")
print("Manual mode or Auto mode")
Request_of_user = str(input("Enter your request: \n", ))
if Request_of_user == "Auto":
    print("Loading Auto mode...")
    from task2 import Task2
    sche.SCH_Add_Task(Task2, 2, 0)

elif Request_of_user == "Manual":
    print("Loading Manual mode...")
    from task3 import Task3
    sche.SCH_Add_Task(Task3, 5, 10)
