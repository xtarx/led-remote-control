import cv2
import sys
import serial
import time
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
ramp_frames = 30
video_capture = cv2.VideoCapture(0)
#video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 500);
#video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600);
#ser = serial.Serial('/dev/cu.usbmodem1411',9600)
#ser.write(str.encode('0'))

#ser.write(str.encode('2'))

# Captures a single image from the camera and returns it in PIL format
def get_image():
 # read is the easiest way to get a full image out of a VideoCapture object.
 retval, im = video_capture.read()
 return im
 
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
for i in xrange(ramp_frames):
 temp = get_image()
print("Taking image...")
# Take the actual image we want to keep
camera_capture = get_image()
file = "test_image.png"
# A nice feature of the imwrite method is that it will automatically choose the
# correct format based on the file extension you provide. Convenient!
cv2.imwrite(file, camera_capture)
 
get_image()
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(video_capture)

while True:
    #print(video_capture.isOpened()

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(200, 200),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print "Found {0} faces!".format(len(faces))
    state = 0

    if len(faces)>4 and state != 1:
        print('in the iuf')
        #ser.write(str.encode('3'))
        state = 1   
        time.sleep(1)
    else:
        #ser.write(str.encode('0'))
        state=0
        time.sleep(1)

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
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    if frame is not None:
        cv2.imshow('Video', frame)

    # time.sleep(0.5)
    if cv2.waitKey(300) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
