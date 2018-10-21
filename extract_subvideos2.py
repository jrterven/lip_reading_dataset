from src import detect_faces, show_bboxes
import numpy as np
import cv2
import re
import os
import math
import datetime
import json
from natsort import natsorted

videos_directory = '/datasets/Our_dataset'
results_dir = '/datasets/Our_dataset/results2'
vids_name = 'TED'
vid_proc_name = 'videos_processed.dat'
scale = 0.5
max_bad_frames = 5
min_area = 2500

def main():

    # Create video window
    cv2.namedWindow('Original')

    # TODO: open or create list with processed files
    videos_processed_exists = os.path.isfile(os.path.join(results_dir, vid_proc_name))
    if not videos_processed_exists:
        f= open(os.path.join(results_dir, vid_proc_name),"r")
    # TODO:  load processed files

    # Get json files list names in videos directory
    files_list = []
    for ann_file in os.listdir(os.path.join(videos_directory, vids_name)):
        if ann_file.endswith(".json"):
            files_list.append(ann_file[0:-6])
    files_list = natsorted(files_list)

    num_files = len(files_list)
    print('found', num_files, 'files')

    # traverse all the files
    for file in files_list:
        # Search for the video files in videos_directory
        video_name = file + '.mp4'
        print('Processing video:', video_name)

        #TODO: check if current video is not in alredy processed files

        # Load watson results
        with open(os.path.join(videos_directory, file + '.json')) as f:
            stt_results = json.load(f)

        # Extract all the words with confidence >90
        words_data = extract_words_from_watson_results(stt_results, max_words=5)

        # Start the video capture
        cap = cv2.VideoCapture(os.path.join(videos_directory, video_name))

        # Extract video metadata
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print('video resolution:', width, ' x ', height)
        print('video framerate:', fps)

        frame_count = 0
        fps_processing = 30.0  # fps holder
        t = cv2.getTickCount() # initiate the tickCounter
        count = 0


        for entry in enumerate(words_data):
            # Extract subtitle data
            start_time = entry['start']
            end_time = entry['end']

            # Determine video frames involved in this subtitle
            min_frame = s_min*fps*60 + (s_sec*fps)
            max_frame = e_min*fps*60 + (e_sec*fps)

            # go to min_frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, min_frame)

            frame_count = min_frame
            # read frames from min_frame to max_frame
            num_people = 0
            
            valid_video = True
            bbx1 = []
            bby1 = []
            bbx2 = []
            bby2 = []
            consecutive_frames_no_people = 0
            while frame_count < max_frame:    
                if count == 0:
                    t = cv2.getTickCount()

                # capture next frame
                ret, frame = cap.read()

                if not ret:
                    continue

                frame_count += 1

                # resize frame for faster processing
                if frame.shape[0] <= 0 or frame.shape[1] <= 0:
                    continue
                    
                frame_small = cv2.resize(frame, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

                # detect faces and landmarjs
                bounding_boxes, landmarks = detect_faces(frame_small)
                num_people = bounding_boxes.shape[0]

                bounding_boxes /= scale
                landmarks /= scale

                # if it detects less than or more than 1 person, go to next subtitle
                if num_people != 1:                    
                    consecutive_frames_no_people += 1
                    
                if consecutive_frames_no_people >= max_bad_frames:
                    print(consecutive_frames_no_people,
                            ' frames without 1 person. Skiping to next subtitle')
                    valid_video = False
                    break
                
                # if only one person in the scene
                if num_people == 1:
                    consecutive_frames_no_people = 0

                    # extract the bounding box
                    bb = bounding_boxes[0]
                    x1, y1, x2, y2 = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])

                    area = (x2 - x1) * (y2 - y1)
                    if area < min_area:
                        valid_video = False
                        #print('area = ', area, ' skiping to next subtitle.')
                        break

                    # save bounding box coordinates for final crop
                    bbx1.append(x1)
                    bbx2.append(x2)
                    bby1.append(y1)
                    bby2.append(y2)

                    # draw the bounding box and landmarks on original frame
                    frame = show_bboxes(frame, bounding_boxes, landmarks)

                    # Put fps at which we are processinf camera feed on frame
                    cv2.putText(frame, "{0:.2f}-fps".format(fps_processing),
                                (50, height-50), cv2.FONT_HERSHEY_COMPLEX,
                                1, (0, 0, 255), 2)

                # Display the image
                cv2.imshow('Original',frame)
            
                # Read keyboard and exit if ESC was pressed
                
                k = cv2.waitKey(1) & 0xFF
                if k ==27:
                    exit()

                # increment frame counter
                count = count + 1
                # calculate fps at an interval of 100 frames
                if (count == 30):
                    t = (cv2.getTickCount() - t)/cv2.getTickFrequency()
                    fps_processing = 30.0/t
                    count = 0

            # if this was a valid video
            if valid_video and len(bbx1) > 0:
                num_output_video += 1

                # get final coordinates
                bbx1 = np.amin(np.array(bbx1))
                bbx2 = np.amax(np.array(bbx2))
                bby1 = np.amin(np.array(bby1))
                bby2 = np.amax(np.array(bby2))
                bbw = bbx2 - bbx1
                bbh = bby2 - bby1

                s_hr = 0
                e_hr = 0
                if s_min >= 60:
                    s_hr = math.floor(s_min / 60)
                    s_min = s_min % 60
                if e_min >= 60:
                    e_hr = math.floor(e_min / 60)
                    e_min = e_min % 60

                # cut and crop video
                # ffmpeg -i input.mp4 -ss hh:mm:ss -filter:v crop=w:h:x:y -c:a copy -to hh:mm:ss output.mp4
                ss = "{0:02d}:{1:02d}:{2:02d}".format(s_hr, s_min, s_sec)
                es = "{0:02d}:{1:02d}:{2:02d}".format(e_hr, e_min, e_sec)
                crop = "crop={0:1d}:{1:1d}:{2:1d}:{3:1d}".format(bbw, bbh, bbx1, bby1)

                out_name = os.path.join(output_dir, str(num_output_video))

                subprocess.call(['ffmpeg', #'-hide_banner', '-loglevel', 'panic',
                                '-i', os.path.join(videos_directory, video_name), '-ss', ss,
                                '-filter:v', crop, '-c:a', 'copy', '-to', es,
                                out_name +'.mp4'])

                # save subtitles
                # text_file = open(out_name +'_sub.txt', "w")
                # text_file.write(text)
                # text_file.close()

                # extract audio from video crop
                if os.path.isfile(out_name+'.mp4'):
                    #ffmpeg -i /home/juan/Videos/ted/1.mp4 -acodec pcm_s16le -ac 1 -ar 16000 out.wav
                    subprocess.call(['ffmpeg', #'-hide_banner', '-loglevel', 'panic',
                                    '-i', out_name+'.mp4',
                                    '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000',
                                    out_name +'.wav'])

                if os.path.isfile(out_name+'.wav'):
                    # recognize audio
                    with sr.AudioFile(out_name +'.wav') as source: audio = r.record(source)
                    try:
                        speech = r.recognize_google(audio, language='es-MX')
                    except sr.UnknownValueError:
                        print('Unknow conversion error')
                        speech = []

                    # save recognized speech
                    if speech:
                        text_file = open(out_name +'_sp.txt', "w")
                        text_file.write(speech)
                        text_file.close()
                    else:
                        os.remove(out_name+'.mp4')

                    # delete audio file
                    os.remove(out_name +'.wav')
                
        
            # Release resources
            cap.release()
            cv2.destroyAllWindows()

def extract_text_conf_ts(s_idx, max_words, num_words, timestamps, conf, link):
    text = ''
    avg_conf = 0
    start = timestamps[int(s_idx * max_words)][1]
    end = timestamps[int(s_idx * max_words + num_words-1)][2]
    
    for w_idx in range(num_words):
        text = text + ' ' + timestamps[int(s_idx*max_words + w_idx)][0]
        avg_conf += conf[int(s_idx*max_words + w_idx)][1]

    avg_conf = round(avg_conf/num_words, 2)
    if len(text.strip()) >= 4:
        out_entry = {'text': text.strip(), 'conf': avg_conf,
                     'start':start, 'end': end,
                     'link': link}
    else:
        out_entry = {}
    return out_entry
    
def extract_words_from_watson_results(stt_results, max_words=5):
    data = stt_results['results']
    link = stt_results['link']
    link = link.rsplit('/', 1)[-1]
    out_data = []
    for sentence_idx, ann in enumerate(data):
        data_ann = ann['alternatives'][0]
        text = data_ann['transcript']
        conf = data_ann['word_confidence']
        timestamps = data_ann['timestamps']
        num_words = len(timestamps)
        num_splits = num_words//max_words
        rest = num_words%max_words

        if num_words < max_words:
            maxx_words = num_words
        else:
            maxx_words = max_words
        
        for s_idx in range(num_splits):
            out_entry = extract_text_conf_ts(s_idx, maxx_words, maxx_words,
                                             timestamps, conf, link)
            out_data.append(out_entry)
        
        if rest > 0:
            out_entry = extract_text_conf_ts(num_splits, maxx_words, rest,
                                         timestamps, conf, link)
            if out_entry:
                out_data.append(out_entry)
            
    return out_data

if __name__== "__main__":
    main()
