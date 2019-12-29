from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import WatsonApiException
import json
import pyaudio
import wave

def TextToSpeech(text, api, url):
    text_to_speech = TextToSpeechV1(
        iam_apikey = api,
        url= url
    )

    text_to_speech.set_default_headers({'x-watson-learning-opt-out': "true"})

    #voice = text_to_speech.get_voice('en-US_AllisonVoice').get_result()
    #voices = text_to_speech.list_voices().get_result()
    #print(json.dumps(voices, indent=2))
    #print(json.dumps(voice, indent=2))

    with open('test.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text,
                'audio/wav',
                'en-US_AllisonVoice'
            ).get_result().content)
    audio_file.close()

def PlayWavFile(wavFileName):
    # define stream chunk
    chunk = 1024

    # open a wav format music
    audio_file = wave.open(wavFileName, "rb")
    # instantiate PyAudio
    play_audio = pyaudio.PyAudio()
    # open stream
    stream = play_audio.open(format=play_audio.get_format_from_width(audio_file.getsampwidth()),
                    channels=audio_file.getnchannels(),
                    rate=audio_file.getframerate(),
                    output=True)
    # read data
    data = audio_file.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = audio_file.readframes(chunk)

        # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    play_audio.terminate()

def TextToSpeechToRead(text, api, url):
    TextToSpeech(text, api, url)
    PlayWavFile('test.wav')
