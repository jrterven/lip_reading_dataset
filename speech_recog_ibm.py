import json
from watson_developer_cloud import SpeechToTextV1

IBM_USERNAME = ""
IBM_PASSWORD = ""

speech_to_text = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)

audio_file = open("/datasets/Our_dataset/results/TED/9/1.wav", "rb")
 #with open('transcript_result.json', 'w') as fp:
result = speech_to_text.recognize(audio_file, content_type="audio/wav",
                        model='es-ES_BroadbandModel',
                        timestamps=True, word_confidence=True).get_result()

print(result)
print(type(result))                           

print(result[''])