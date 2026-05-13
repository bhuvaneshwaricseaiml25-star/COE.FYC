import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

# Path to images
path = 'images'

images = []
classNames = []

myList = os.listdir(path)

print("Loaded Images:", myList)

# Load images and names
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)

# Encode faces
def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 0:
            encode = encodings[0]
            encodeList.append(encode)

    return encodeList

# Mark attendance
def markAttendance(name):
    with open('attendance.csv', 'a+') as f:
        f.seek(0)
        myDataList = f.readlines()

        nameList = []

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')

            f.writelines(f'\n{name},{dtString}')

            print(f'Attendance Marked for {name}')

# Encode known faces
encodeListKnown = findEncodings(images)

print('Encoding Complete')

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    # Resize for faster processing
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    # Find faces
    facesCurFrame = face_recognition.face_locations(imgSmall)
    encodesCurFrame = face_recognition.face_encodings(
        imgSmall,
        facesCurFrame
    )

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):

        # Compare faces
        matches = face_recognition.compare_faces(
            encodeListKnown,
            encodeFace
        )

        faceDis = face_recognition.face_distance(
            encodeListKnown,
            encodeFace
        )

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:

            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc

            # Scale back up
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            # Draw rectangle
            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Name box
            cv2.rectangle(
                img,
                (x1, y2-35),
                (x2, y2),
                (0, 255, 0),
                cv2.FILLED
            )

            cv2.putText(
                img,
                name,
                (x1+6, y2-6),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 255, 255),
                2
            )

            markAttendance(name)

    cv2.imshow('Smart Attendance System', img)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
