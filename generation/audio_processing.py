class AudioProcessing:
  def __init__(self, client):
    self.client = client

  def generate_audio_from_text(self,text,path, provider='default', client=None): 
    pass

  def generate_subtitles(self, audio_path):
    pass

  def openai_tts(self, text, path, client):
    response = client.audio.speech.create(
      model="tts-1",
      voice="onyx",
      input=text
    )

    return response

  def elevenlabs_tts(self, text, path):
    pass

  def speed_up_audio(self, speech_file_path, speed_factor=1.5):
    pass
