from core import Core, capture_image
import time


with Core(
    mean_history=3,           # number of frames for which you keep track of mean
    max_faces_allowed=1,      # the max number of people allowed in scene
    camera1=0,
    camera2=2,
    speak=False,
    display_faces=True
) as core:

    t1 = time.time()
    while True:
        #camera 1
        frame = capture_image(core.video_capture1)
        core.face_extractor(1,frame)

        #camera 2
        frame = capture_image(core.video_capture2)
        core.face_extractor(2, frame)


        # time.sleep(sleep_interval)
        curtime = time.time()
        print("Loop Time is: ", curtime-t1)
        t1 = time.time()