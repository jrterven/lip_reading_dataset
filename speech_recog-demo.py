import speech_recognition as sr

# ffmpeg -i /home/juan/Videos/ted/1.mp4 -acodec pcm_s16le -ac 1 -ar 16000 out.wav
AUDIO_FILE_EN = '/home/juan/dev/lip_reading_dataset/out.wav'

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE_EN) as source: audio = r.record(source)

try:
    text1 = r.recognize_google(audio, language='es-MX')
except sr.UnknownValueError:
    print('Unknow conversion error')

print(text1)



