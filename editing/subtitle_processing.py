
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
    sentence_lengths = [len(sentence.split(" ")) for sentence in transcript_array]

    word_index = 0
    words = subtitles["words"]

    for sentence_length in sentence_lengths:
        word_count = 0
        start_index = word_index
        while word_count < sentence_length and word_index < len(words):
            word_count += 1
            word_index += 1
        
        start_time = words[start_index]["start"] if start_index < len(words) else 0
        end_time = words[word_index - 1]["end"] if word_index - 1 < len(words) else words[-1]["end"]
        image_timestamps.append({"start": start_time, "end": end_time})

    return image_timestamps
  