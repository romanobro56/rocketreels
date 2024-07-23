from pydub.silence import split_on_silence
from pydub import AudioSegment
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
      raise(SystemError("TTS Voices other than OpenAI not yet supported"))

    # Stream the audio response into the file path
    response.stream_to_file(output_path)

    final_audio = self.replace_long_silence(output_path)
    final_audio.export(output_path, format="mp3")

  def openai_tts(self, text, client, chosen_voice):
    response = client.audio.speech.create(
      model="tts-1",
      voice=chosen_voice,
      input=text
    )

    return response

  def replace_long_silence(self, audio_path, silence_thresh=-50, min_silence_len=500, silence_replacement_len=50):
    audio = AudioSegment.from_file(audio_path)
    chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    short_silence = AudioSegment.silent(duration=silence_replacement_len)
    processed_audio = AudioSegment.empty()
    for chunk in chunks:
      processed_audio += chunk + short_silence

    processed_audio = processed_audio[:-silence_replacement_len]

    return processed_audio