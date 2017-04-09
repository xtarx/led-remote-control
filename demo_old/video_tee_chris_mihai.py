import cv2
import serial
import time
import os
import face_recognition
from os import system

dir = os.path.dirname(__file__)
import numpy as np
sleep_interval=1
ramp_frames = 30
video_capture = cv2.VideoCapture(0)
video_capture_2 = cv2.VideoCapture(2)
cv2.resizeWindow('Video', 600,600)

cv2.namedWindow("camera1", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("camera2",cv2.WINDOW_AUTOSIZE)

ser = serial.Serial('/dev/cu.usbmodem14141',9600)
ser.write(str.encode('0'))


# use

class MeanStream:
    def __init__(self, size):
        self.size = float(size)
        self.accumulated = 0.
        self.numbers = [0]*size
        self._mean = 0.

    def add(self, num):
        i = int(self.accumulated) % int(self.size)
        self.accumulated += 1
        if self.accumulated <= self.size:
            self._mean = self._mean*(self.accumulated-1) + num
            self._mean /= self.accumulated
            self.numbers[i] = num
        else:
            self._mean = self._mean*self.size - self.numbers[i] + num
            self._mean /= self.size
            self.numbers[i] = num


    @property
    def mean(self):
        return self._mean




def faceExtractor(camera, frame):
    if frame is not None:
        faces = face_recognition.face_locations(frame)
        print "Camera:{0} Found {1} faces!".format(camera, len(faces))
        visualiseLed(camera, len(faces))
        # speak(camera, len(faces))
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

# def visualiseLed(camera, faces_count):
#     if faces_count > faces_threshold_busy:
#         if camera == 1:
#             ser.write(str.encode('1'))
#         else:
#             ser.write(str.encode('3'))
#
#     elif faces_count < face_threshold_free:
#         if camera == 1:
#             ser.write(str.encode('5'))
#         else:
#             ser.write(str.encode('7'))


# # STATES

busy1 = False
busy2 = False
max_frames = 3

faces_threshold_busy = 4.
face_threshold_free = 3.


mean1 = MeanStream(max_frames)
mean2 = MeanStream(max_frames)


def visualiseLed(camera, faces_count, states=False):
    global busy1, busy2
    if camera == 1:
        mean1.add(faces_count)
        if mean1.mean >= faces_threshold_busy:
            if states and busy1:
                return
            ser.write(str.encode('1'))
            busy1 = True
        elif mean1.mean <= face_threshold_free:
            if states and not busy1:
                return
            ser.write(str.encode('5'))
            busy2 = False
    else:
        mean2.add(faces_count)
        if mean2.mean >= faces_threshold_busy:
            if states and busy2:
                return
            ser.write(str.encode('3'))
            busy2 = True
        elif mean2.mean <= face_threshold_free:
            if states and not busy2:
                return
            ser.write(str.encode('7'))
            busy2 = False


    #
    #
    # if faces_count >= faces_threshold_busy:
    #     if camera == 1 and not busy1:
    #         ser.write(str.encode('1'))
    #         busy1 = True
    #     elif camera == 2 and not busy2:
    #         busy2 = True
    #         ser.write(str.encode('3'))
    #
    # elif faces_count <= face_threshold_free:
    #     if camera == 1 and busy1:
    #         ser.write(str.encode('5'))
    #         busy1 = False
    #     elif camera == 2 and busy2:
    #         ser.write(str.encode('7'))
    #         busy2 = False



# maxcam1 = 0
# maxcam2 = 0
# vi1 = 0
# vi2 = 0
# max_frames = 2
# def visualiseLed(camera, faces_count):
#     global faces_threshold_busy, face_threshold_free, maxcam1, maxcam2, vi1, vi2
#     if camera == 1:
#         maxcam1 = max(maxcam1, faces_count)
#         if vi1 == max_frames:
#             if maxcam1 > faces_threshold_busy:
#                 ser.write(str.encode('1'))
#             elif maxcam1 < face_threshold_free:
#                 ser.write(str.encode('5'))
#             maxcam1 = 0
#             vi1 = 0
#     else:
#         maxcam1 = max(maxcam1, faces_count)
#         if vi2 == max_frames:
#             if maxcam2 > faces_threshold_busy:
#                 ser.write(str.encode('3'))
#             elif maxcam2 < face_threshold_free:
#                 ser.write(str.encode('7'))
#             maxcam2 = 0
#             vi2 = 0


def getSharpness(frame):
    # dst = np.zeros(frame.shape)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    dst = cv2.Laplacian(gray, 2)
    maxLap = -2**31
    for i in range(dst.shape[0]):
        for j in range(dst.shape[1]):
            maxLap = max(dst[i][j], maxLap)
    return maxLap

def capture_image(video_capture):
    ret, frame = video_capture.read()
    while frame is None:
        ret, frame = video_capture.read()
    return frame

t1 = time.time()
while True:
    #camera 1
    frame = capture_image(video_capture)
    faceExtractor(1,frame)
    # print ("sharpenes!!!! - camera 1", getSharpness(frame))

    #camera 2
    frame = capture_image(video_capture_2)
    faceExtractor(2, frame)
    # print ("sharpenes!!!! - camera 2", getSharpness(frame))

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     ser.write(str.encode('0'))
    #     break
    # time.sleep(sleep_interval)
    curtime = time.time()
    print("TIME: ", curtime-t1)
    t1 = time.time()

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()