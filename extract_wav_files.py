import os
import pandas as pd
import subprocess

directory = '/datasets/Our_dataset'
selected_cat = 'CNN'

# Read file names in videos directory
video_names = []
for video_file in os.listdir(os.path.join(directory, selected_cat)):
    if video_file.endswith(".mp4"):
        video_names.append(video_file)

num_files = len(video_names)
print('found', num_files, 'files')
#print(video_names)

# Read spreadsheet
df = pd.read_excel(os.path.join(directory, selected_cat +'.xlsx'))

for video_name in video_names:
    # For each video file, check if the link is available
    data = df[df['Video'].str.contains(video_name[:-4])==True]

    if data.shape[0] == 0:
        print('Not found in spredsheet:', video_name)

    print('Extracting wav file from ', video_name)
    # extract the wav file
    video_path = os.path.join(directory, selected_cat, video_name)
    out_wave_path = video_path[:-4] + '.wav'
    #ffmpeg -i video.mp4 -acodec pcm_s16le -ac 1 -ar 16000 out.wav
    subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'panic',
                    '-i', video_path, '-acodec', 'pcm_s16le', '-ac', '1',
                    '-ar', '16000', out_wave_path])
        

    