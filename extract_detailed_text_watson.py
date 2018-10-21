import os
import pandas as pd
import subprocess
from watson_developer_cloud import SpeechToTextV1
import json
from natsort import natsorted

directory = '/datasets/Our_dataset'
selected_cat = 'holasoygerman'

IBM_USERNAME = ""
IBM_PASSWORD = ""

speech_to_text = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)

# Read wave file names in videos directory
audio_names = []
for video_file in os.listdir(os.path.join(directory, selected_cat)):
    if video_file.endswith(".wav"):
        audio_names.append(video_file)
audio_names = natsorted(audio_names)

num_files = len(audio_names)
print('found', num_files, 'files')
#print(audio_names)

# Read spreadsheet
df = pd.read_excel(os.path.join(directory, selected_cat +'.xlsx'))

for audio_name in audio_names:
    # For each video file, check if the link is available
    data = df[df['Video'].str.contains(audio_name[:-4])==True]

    link = ''

    if data.shape[0] == 0:
        print('Not found in spredsheet:', audio_name)
    else:
        link = data.iloc[0]['Link']

        # Extract text using Watson
        print('Extracting detailed text using Watson for', audio_name)
        audio_path = os.path.join(directory, selected_cat, audio_name)

        with open(audio_path, "rb") as audio_file:
            result = speech_to_text.recognize(audio_file, content_type="audio/wav",
                            model='es-ES_BroadbandModel',
                            timestamps=True, word_confidence=True).get_result()
            
            # add the link to the results
            result['link'] = link

            # save json file
            out_json_path = audio_path[:-4] + '.json'
            with open(out_json_path, 'w') as outfile:
                json.dump(result, outfile)

    