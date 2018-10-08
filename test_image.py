from src import detect_faces, show_bboxes
import numpy as np
import cv2
import time

img = cv2.imread('/home/juan/Documents/cv_course/data/images/family.jpg',cv2.IMREAD_COLOR)

start_time = time.time()
frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
bounding_boxes, landmarks = detect_faces(img)
duration = time.time() - start_time
print('Face detector and landmark time: %.3fs' % duration)
print("Number of faces detected: ",bounding_boxes.shape[0])

img = show_bboxes(img, bounding_boxes, landmarks)

cv2.imshow('Image', img)

cv2.waitKey(0)
