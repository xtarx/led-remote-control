import cv2
import numpy as np
import sys



# cascPath = sys.argv[1]
# faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier('./HS.xml')
# faceCascade = cv2.CascadeClassifier('./haarcascadqe_frontalface_alt_tree.xml')

cap = cv2.VideoCapture(0) # Capture video from camera

# Get the width and height of frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))



while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # write the flipped frame

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        print("Found {0} faces!".format(len(faces)))
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        out.write(frame)
        cv2.imshow('frame',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break
    else:
        break


# Release everything if job is finished
out.release()
cap.release()
cv2.destroyAllWindows()



