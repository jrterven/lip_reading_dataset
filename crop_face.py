from src import detect_faces, show_bboxes
import numpy as np
import cv2
import pysrt
import re

PROCESS_VIDEO = False

def main():
    # Load the subtitles
    subs = pysrt.open('/home/juan/Videos/AMOR.es.srt', encoding='iso-8859-1')

    # Start the video capture
    cap = cv2.VideoCapture('/home/juan/Videos/AMOR.mp4')
    
    cv2.namedWindow('Original')
    cv2.namedWindow('Cropped')

    # Extract number of subtitles
    num_subs = len(subs)
    print('Num subtitles:', num_subs)

    # Extract video metadata
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('video resolution:', width, ' x ', height)
    print('video framerate:', fps)

    cv2.waitKey(0)

    for s_idx, sub in enumerate(subs):
        s = "{0:1d}, {1:02d}:{2:02d} to {3:02d}:{4:02d} {5:s}"
        text = cleanhtml(sub.text)
        print(s.format(s_idx, sub.start.minutes, sub.start.seconds,
            sub.end.minutes, sub.end.seconds, text))

    while True:             
        # capture next frame
        ret, frame = cap.read()

        if PROCESS_VIDEO:
            # resiz frame for faster processing
            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

            # detect faces and landmarjs
            bounding_boxes, landmarks = detect_faces(frame)
            
            # if only one face detected
            if bounding_boxes.shape[0] == 1:
                # extract the bounding box
                bb = bounding_boxes[0]
                x1, y1, x2, y2 = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])
            
                # crop the face
                cropped = frame[y1:y2, x1:x2]
                cv2.imshow('Cropped', cropped)

            # draw the bounding box and landmarks on original frame
            frame = show_bboxes(frame, bounding_boxes, landmarks)

        # Display the image
        cv2.imshow('Original',frame)
    
        # Read keyboard and exit if ESC was pressed
        k = cv2.waitKey(10) & 0xFF
        if k ==27:
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

if __name__== "__main__":
    main()
