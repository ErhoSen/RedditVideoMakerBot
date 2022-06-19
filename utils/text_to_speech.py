from google.api_core.client_options import ClientOptions
from google.cloud import texttospeech_v1beta1 as texttospeech


# noinspection PyTypeChecker
class TTSClient:

    def __init__(self):
        client_options = ClientOptions(
            credentials_file="google_credentials.json",
        )
        self.client = texttospeech.TextToSpeechClient(client_options=client_options)
        self.voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            name='en-US-Wavenet-F'
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0,
            volume_gain_db=0.0
        )

    def list_voices(self):
        voices = self.client.list_voices(language_code='en-US')
        for voice in voices.voices:
            print(f"Name: {voice}")

    def get_audio(self, text) -> bytes:
        input_text = texttospeech.types.SynthesisInput(text=text)
        response = self.client.synthesize_speech(input=input_text, voice=self.voice, audio_config=self.audio_config)
        return response.audio_content


tts_client = TTSClient()
