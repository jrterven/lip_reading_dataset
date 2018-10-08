import json
from watson_developer_cloud import SpeechToTextV1

IBM_USERNAME = "jrterven@hotmail.com"
IBM_PASSWORD = "Jack1958"

stt = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)
audio_file = open("/home/juan/ted01.wav", "rb")


with open('transcript_result.json', 'w') as fp:
    result = stt.recognize(audio_file, content_type="audio/x-flac",
                           continuous=True, timestamps=True,
                           max_alternatives=1)
    json.dump(result, fp, indent=2)