import cv2
import sys
import serial
import time

cascPath = sys.argv[1]
sleep_interval=1
faceCascade = cv2.CascadeClassifier(cascPath)
ramp_frames = 30
video_capture = cv2.VideoCapture(0)
cv2.resizeWindow('Video', 600,600)

# video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 500);
# video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600);
#ser = serial.Serial('/dev/cu.usbmodem1D1121',9600)

while True:
    # print(video_capture.isOpened()
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(300, 300),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
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

    # width = frame.shape[1]
    # if len(faces):
    #     face = max(faces, key=lambda a: abs(a[2]*a[3]))
    #     current = face[0] + face[2]/2
    #     if current < width/3. and state != 1:
    #         ser.write(str.encode('1'))
    #         state=1
    #     elif current>= width/3. and current < 2.*width/3. and state != 2:
    #         ser.write(str.encode('2'))
    #         state=2
    #     elif current > 2.*width/3. and state != 3:
    #         ser.write(str.encode('3'))
    #         state=3
    # elif state:
    #     ser.write(str.encode('0'))
    #     state=0
    # print("STATE is ", state)


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