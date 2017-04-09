import cv2
import os
import face_recognition
from arduino_api import CrowdLessArduinoConnection
from mean_stream import MeanStream


def capture_image(video_capture):
    ret, frame = video_capture.read()
    cv2.waitKey(1)
    while frame is None:
        ret, frame = video_capture.read()
        cv2.waitKey(1)

    return frame


def speak_count_faces(camera, n_faces):
    sp = "Camera {0} Found {1} faces!".format(camera, n_faces)
    os.system('say ' + sp)


class Core:
    def __init__(self, mean_history=3, max_faces_allowed=6, camera1=0, camera2=0, speak=False, display_faces=True,  use_states=True):
        self.faces_threshold_busy = .75 * max_faces_allowed
        self.face_threshold_free = .5 * max_faces_allowed

        self.mean1faces = MeanStream(mean_history)
        self.mean2faces = MeanStream(mean_history)

        self.camera1_is_busy = False
        self.camera2_is_busy = False

        self.use_states = use_states

        self.video_capture1 = cv2.VideoCapture(camera1)
        self.video_capture2 = cv2.VideoCapture(camera2)

        self.display_faces = display_faces
        if self.display_faces:
            cv2.namedWindow("camera1", cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow("camera2", cv2.WINDOW_AUTOSIZE)

        self.arduino = CrowdLessArduinoConnection()

        # not recommended to make true because it delays 2 seconds per call
        self.speak = speak

    def face_extractor(self, camera, frame):
        if frame is not None:
            faces = face_recognition.face_locations(frame)
            print "Camera:{0} Found {1} faces!".format(camera, len(faces))
            self.visualize_leds(camera, len(faces))
            if self.speak:
                speak_count_faces(camera, len(faces))
            if self.display_faces:
                # Draw a rectangle around the faces
                for (top, right, bottom, left) in faces:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Display the resulting frame
                imS = cv2.resize(frame, (600, 400))  # Resize image
                cv2.imshow('camera' + str(camera), imS)

    def visualize_leds(self, camera, faces_count):
        if camera == 1:
            self.mean1faces.add(faces_count)
            if self.mean1faces.mean >= self.faces_threshold_busy:
                if self.use_states and self.camera1_is_busy:
                    return
                self.arduino.green_door(1)
                self.camera1_is_busy = True
            elif self.mean1faces.mean <= self.face_threshold_free:
                if self.use_states and not self.camera1_is_busy:
                    return
                self.arduino.red_door(1)
                self.camera1_is_busy = False
        else:
            self.mean2faces.add(faces_count)
            if self.mean2faces.mean >= self.faces_threshold_busy:
                if self.use_states and self.camera2_is_busy:
                    return
                self.arduino.green_door(3)
                self.camera2_is_busy = True
            elif self.mean2faces.mean <= self.face_threshold_free:
                if self.use_states and not self.camera2_is_busy:
                    return
                self.arduino.red_door(3)
                self.camera2_is_busy = False

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.video_capture1.release()
        self.video_capture2.release()
        if self.display_faces:
            cv2.destroyAllWindows()
