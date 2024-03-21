from pydub import AudioSegment

class Utilities:
  
  def format_time(self, seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}".replace('.', ',')
  
  def get_audio_duration(mp3_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)
    duration_milliseconds = len(audio)
    duration_seconds = duration_milliseconds / 1000.0

    return duration_seconds
