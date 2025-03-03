from pydub.silence import split_on_silence
from pydub import AudioSegment
import os 

class AudioProcessor:
  def __init__(self, client, elevenlabs_client=None):
    self.client = client  # OpenAI client
    self.elevenlabs_client = elevenlabs_client  # ElevenLabs client

  def list_elevenlabs_voices(self):
    """Returns a list of available ElevenLabs voices"""
    if not self.elevenlabs_client:
      raise SystemError("ElevenLabs client not initialized")
    
    try:
      response = self.elevenlabs_client.voices.get_all()
      return [(v.voice_id, v.name) for v in response.voices]
    except Exception as e:
      raise SystemError(f"Failed to get ElevenLabs voices: {str(e)}")

  def generate_audio_from_text(self, text, output_path, voice, tts_provider="openai"): 
    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if tts_provider.lower() == "openai":
      openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
      if voice in openai_voices:
        response = self.openai_tts(text, self.client, voice)
        # Stream the audio response into the file path
        response.stream_to_file(output_path)
      else:
        raise(SystemError("Invalid OpenAI voice selected"))
    elif tts_provider.lower() == "elevenlabs":
      self.elevenlabs_tts(text, output_path, voice)
    else:
      raise(SystemError("TTS provider not supported. Use 'openai' or 'elevenlabs'"))

    final_audio = self.replace_long_silence(output_path)
    final_audio.export(output_path, format="mp3")

  def openai_tts(self, text, client, chosen_voice):
    response = client.audio.speech.create(
      model="tts-1-hd",
      voice=chosen_voice,
      input=text
    )

    return response
  
  def elevenlabs_tts(self, text, output_path, voice_id):
    try:
      if self.elevenlabs_client is None:
        raise SystemError("ElevenLabs client not initialized")
      
      # Get the audio stream (generator)
      audio_stream = self.elevenlabs_client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
      )
      
      # Write the audio data to file, handling both generator and bytes cases
      with open(output_path, "wb") as f:
        # Check if audio_stream is a generator or bytes
        if hasattr(audio_stream, '__iter__') and not isinstance(audio_stream, (bytes, bytearray)):
          # It's a generator, consume it and write each chunk
          for chunk in audio_stream:
            if chunk:  # Check that chunk is not None
              f.write(chunk)
        else:
          # It's bytes, write directly
          f.write(audio_stream)
        
      return True
    except Exception as e:
      raise SystemError(f"ElevenLabs TTS failed: {str(e)}")

  def replace_long_silence(self, audio_path, silence_thresh=-50, min_silence_len=500, silence_replacement_len=50):
    audio = AudioSegment.from_file(audio_path)
    chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    short_silence = AudioSegment.silent(duration=silence_replacement_len)
    processed_audio = AudioSegment.empty()
    for chunk in chunks:
      processed_audio += chunk + short_silence

    processed_audio = processed_audio[:-silence_replacement_len]

    return processed_audio