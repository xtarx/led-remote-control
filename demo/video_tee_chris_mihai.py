import cv2
import serial
import time
import os
import face_recognition
from os import system
dir = os.path.dirname(__file__)

sleep_interval=1
ramp_frames = 30
video_capture = cv2.VideoCapture(0)
video_capture_2 = cv2.VideoCapture(2
                                   )
cv2.resizeWindow('Video', 600,600)

cv2.namedWindow("camera1", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("camera2",cv2.WINDOW_AUTOSIZE)

ser = serial.Serial('/dev/cu.usbmodem14141',9600)
ser.write(str.encode('0'))

faces_threshold = 0

def faceExtractor(camera, frame):
    if frame is not None:
        faces = face_recognition.face_locations(frame)
        print "Camera:{0} Found {1} faces!".format(camera, len(faces))
        visualiseLed(camera, faces)
        speak(camera, len(faces))
        # Draw a rectangle around the faces
        for (top, right, bottom, left) in faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the resulting frame
        if frame is not None:
            imS = cv2.resize(frame, (600, 400))  # Resize image
            cv2.imshow('camera'+str(camera), imS)


def speak(camera, n_faces):
    sp = "Camera {0} Found {1} faces!".format(camera, n_faces)
    system('say ' + sp)


def visualiseLed(camera, faces_count):
    if len(faces_count) > faces_threshold:
        if camera == 1:
            ser.write(str.encode('1'))
        else:
            ser.write(str.encode('3'))

    else:
        if camera == 1:
            ser.write(str.encode('5'))
        else:
            ser.write(str.encode('7'))


while True:
    #camera 1
    ret, frame = video_capture.read()
    faceExtractor(1,frame)

    #camera 2
    ret, frame = video_capture_2.read()
    faceExtractor(2, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ser.write(str.encode('0'))
        break
    time.sleep(sleep_interval)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()