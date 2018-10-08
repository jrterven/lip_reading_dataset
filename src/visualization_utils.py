import numpy as np
import cv2


def show_bboxes(img, bounding_boxes, facial_landmarks=[]):
    """Draw bounding boxes and facial landmarks.

    Arguments:
        img: uint8 numpy array of shape [rows, cols, 3]
        bounding_boxes: a float numpy array of shape [n, 5].
        facial_landmarks: a float numpy array of shape [n, 10].

    Returns:
        uint8 numpy array of shape [rows, cols, 3]
    """

    img_copy = np.copy(img)

    for b in bounding_boxes:
        x1, y1, x2, y2 = int(b[0]), int(b[1]), int(b[2]), int(b[3])
        cv2.rectangle(img_copy,(x1, y1),(x2, y2),(255,255,255),2)

    for p in facial_landmarks:
        for i in range(5):
            x, y = p[i], p[i + 5]
            cv2.circle(img_copy, (x,y), 2, (0,0,255), -1)

    return img_copy
