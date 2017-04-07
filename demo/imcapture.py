import cv
capture = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, my_height)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, my_width)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FORMAT, cv.IPL_DEPTH_32F)

img = cv.QueryFrame(capture)