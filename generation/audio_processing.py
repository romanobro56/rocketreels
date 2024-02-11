from pydub.silence import split_on_silence
from pydub import AudioSegment
import whisper
import os 

class AudioProcessor:
  def __init__(self, client):
    self.client = client

  def generate_audio_from_text(self, text, output_path, voice): 
    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    if voice in openai_voices:
      response = self.openai_tts(text, self.client, voice)
    else:
      print("Elevenlabs TTS is not yet supported")
      # response = self.elevenlabs_tts(text, self.client, voice)

    # Stream the audio response into the file path
    response.stream_to_file(output_path)
    self.speed_up_audio(output_path)
    self.lower_pitch(output_path)

    final_audio = self.replace_long_silence(output_path)
    final_audio.export(output_path, format="mp3")

  def openai_tts(self, text, client, chosen_voice):
    response = client.audio.speech.create(
      model="tts-1",
      voice=chosen_voice,
      input=text
    )

    return response
  
  def elevenlabs_tts(self, text, client, chosen_voice):
    pass

  def speed_up_audio(speech_file_path):
    audio = AudioSegment.from_file(speech_file_path)

    sped_up_audio = audio.speedup(playback_speed=1.4)
    sped_up_audio.export(speech_file_path, format="mp3")

  def lower_pitch(audio_path):
    audio = AudioSegment.from_file(audio_path)
    lower_pitch_audio = audio.low_pass_filter(3000)
    lower_pitch_audio.export(audio_path, format="mp3")


  def replace_long_silence(audio_path, silence_thresh=-50, min_silence_len=500, silence_replacement_len=50):
    audio = AudioSegment.from_file(audio_path)
    chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    short_silence = AudioSegment.silent(duration=silence_replacement_len)
    processed_audio = AudioSegment.empty()
    for chunk in chunks:
      processed_audio += chunk + short_silence

    processed_audio = processed_audio[:-silence_replacement_len]

    return processed_audio