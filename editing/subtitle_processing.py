
class SubtitleProcessor:
  def __init__(self, client=None):
    self.client = client

  def generate_subtitles(self, audio_path):
    audio_file = open(audio_path, "rb")

    transcript = self.client.audio.transcriptions.create(
      file=audio_file,
      model="whisper-1",
      response_format="verbose_json",
      timestamp_granularities=["word"]
    )

    return transcript
  
  def get_image_timestamps(self, subtitles, transcript_array):
    image_timestamps = []
    for word in transcript_array:
      for subtitle in subtitles:
        if word in subtitle:
          image_timestamps.append(subtitle)
    return image_timestamps
  