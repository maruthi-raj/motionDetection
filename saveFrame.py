import argparse
import datetime
import imutils
import os
import cv2
import numpy as np
import time
from time import sleep

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-s", "--size", type=int, default=480, help="minimum area size , default 480")
args = vars(ap.parse_args())

#set the directory in which the frames should be saved
directory=r"E:\videos"
os.chdir(directory)


# if no video use webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)

# use video file
else:
    camera = cv2.VideoCapture(args["video"])

first_frame = None

while True:
    # grab the current frame 
    (grabbed, frame) = camera.read()
    text = "undetected"

    # is no frame grabbed the is end of video 
    if not grabbed:
        break

    # resize the frame 
    frame = imutils.resize(frame, width=800) #width=640
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # is first frame is none , make gray 
    if first_frame is None:
        first_frame = gray
        continue


    # compute difference from current frame and first frame 
    frameDelta = cv2.absdiff(first_frame, gray)
    first_frame = gray
    thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]

    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
    
    # loop for contours on the binary frame
    for c in cnts:

        # if the contour size is too small, ignore it
        if cv2.contourArea(c) < args["size"]:
            continue
        #else
        # compute the bounding box for the contour and draw it on the frame
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 0)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')
        # if detection is of a good size then save the frame
        if (w > h ) and (y + h) > 50 and (y + h) < 550:
            cv2.imwrite(st+"opencv.jpg",frame)
    
    # draw the text and timestamp on the frame
    cv2.imshow("thres",frame)
    key = cv2.waitKey(1) &  0xFF

    # Use q to break the loop 
    if key == ord("q"):
        break

# close camera and windows 
camera.release()
cv2.destroyAllWindows()