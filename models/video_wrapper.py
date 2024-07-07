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
