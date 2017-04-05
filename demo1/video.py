import cv2
import sys
import serial
import time
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
#video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 500);
#video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600);
ser = serial.Serial('/dev/cu.usbmodem1421',9600)
#ser.write(str.encode('2'))
while True:
    #print(video_capture.isOpened()

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(150, 150),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    print "Found {0} faces!".format(len(faces))
    if len(faces)>2 :
        print('in the iuf')
        ser.write(str.encode('2'))
        time.sleep(1)
    else:
        ser.write(str.encode('0'))
        time.sleep(1)




    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    if frame is not None:
        cv2.imshow('Video', frame)


    if cv2.waitKey(300) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
