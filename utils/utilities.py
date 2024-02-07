class Utilities:
  def format_time(self, seconds):
    """
      Convert seconds to a time string in the format HH:MM:SS
      Useful for taking time in seconds and converting it to SRT format
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}".replace('.', ',')