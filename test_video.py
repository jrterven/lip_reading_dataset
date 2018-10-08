from src import detect_faces, show_bboxes
import numpy as np
import cv2

# Start the video capture
cap = cv2.VideoCapture('/home/juan/Videos/ted/ted01.mp4')
 
# Extract video metadata
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = cap.get(cv2.CAP_PROP_FPS)
print('video resolution:', width, ' x ', height)
print('video framerate:', fps)

fps = 30.0

# initiate the tickCounter
t = cv2.getTickCount()
count = 0

while True:           
    if count == 0:
        t = cv2.getTickCount() 

    # capture next frame
    ret, frame = cap.read()

    #frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

    bounding_boxes, landmarks = detect_faces(frame)

    # render frame
    frame = show_bboxes(frame, bounding_boxes, landmarks)

    # Put fps at which we are processinf camera feed on frame
    cv2.putText(frame, "{0:.2f}-fps".format(fps), (50, height-50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 3)

    # Display the image
    cv2.imshow('frame',frame)
 
    # Read keyboard and exit if ESC was pressed
    k = cv2.waitKey(10) & 0xFF
    if k ==27:
        break

    # increment frame counter
    count = count + 1
    # calculate fps at an interval of 100 frames
    if (count == 30):
        t = (cv2.getTickCount() - t)/cv2.getTickFrequency()
        fps = 30.0/t
        count = 0
 
# Release resources
cap.release()
cv2.destroyAllWindows()


