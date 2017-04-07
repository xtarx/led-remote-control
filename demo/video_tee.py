import cv2
import sys
import serial
import time
import os

sleep_interval=1
faceCascade = cv2.CascadeClassifier('Face_cascade.xml')
ramp_frames = 30
video_capture = cv2.VideoCapture(0)
cv2.resizeWindow('Video', 600,600)

#ser = serial.Serial('/dev/cu.usbmodem1D1121',9600)

while True:
    # print(video_capture.isOpened()
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.16, minNeighbors=5, minSize=(25, 25), flags=0
    )

    print "Found {0} faces!".format(len(faces))
    state = 0

    if len(faces) > 2 and state != 1:
        print('in the iuf')
        #ser.write(str.encode('3'))
        state = 1
        #time.sleep(1)
    else:
        #ser.write(str.encode('0'))
        state = 0
        #time.sleep(1)

    # state = 0


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    if frame is not None:
        imS = cv2.resize(frame, (960, 540))  # Resize image
        cv2.imshow('Video', imS)
        # cv2.imshow(imS)


    # time.sleep(0.5)
    if cv2.waitKey(300) & 0xFF == ord('q'):
        break
    time.sleep(sleep_interval)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()