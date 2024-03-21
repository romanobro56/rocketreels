from moviepy.editor import VideoFileClip

class VideoWrapper:
    def __init__(self, video_path, client=None):
        self.video_path = video_path
        self.client = client

        try:
          self.video_clip = VideoFileClip(video_path)
        except OSError as e:
          raise ValueError(f"Error loading video: {e}") from e
        except Exception as e:  # Catch other potential MoviePy errors
          raise ValueError(f"Unexpected error loading video: {e}") from e


    def get_runtime(self):
        # Returns the duration of the video in seconds
        return self.video_clip.duration

    def generate_subtitles(self):
      if not self.client:
        raise ValueError("Transcription client not configured.")

      # Full audio extraction with moviepy    
      audio_file = self.video_clip.audio
      temp_audio_path = "temp_audio.mp3"  # Or a suitable format for your service
      audio_file.write_audiofile(temp_audio_path)

      with open(temp_audio_path, "rb") as audio:

        transcript = self.client.audio.transcriptions.create(
          file=audio_file,
          model="whisper-1",
          response_format="verbose_json",
          timestamp_granularities=["word"]
        )

      audio_file.close()
      return transcript
    
    def get_aspect_ratio(self):
        return self.video_clip.size[0] / self.video_clip.size[1]

    def get_resolution(self):
        return self.video_clip.size
    
    def get_frame_rate(self):
        return self.video_clip.fps
    
    def get_duration(self):
        return self.video_clip.duration

