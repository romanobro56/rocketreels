from editing.subtitle_processing import SubtitleProcessor
from editing.video_processing import VideoProcessor
from models.video_wrapper import VideoWrapper

class VideoEditingWorkflow:
  def __init__(self, content_package, video_file_path, editing_options):
    # content package is an instance of MultimediaComposition which contains the content and file paths
    self.content_package = content_package
    self.video_processor = VideoProcessor(editing_options)
    self.subtitle_processor = SubtitleProcessor()
    self.video_file_path = video_file_path

  def generate_video_from_content(self):
    # silent_video_path = self.video_processor.generate_video_from_images(self.content_package, self.video_file_path)
    silent_video_file_clip = VideoWrapper(self.video_file_path + "/outputSilent.mp4")
    subtitled_video_path = self.video_processor.overlay_subtitles(self.content_package, silent_video_file_clip.get_video(), self.video_file_path)
    subtitled_video_file_clip = VideoWrapper(subtitled_video_path)
    final_video_path = self.video_processor.overlay_audio(self.content_package, subtitled_video_file_clip, self.video_file_path)

    self.video_processor.apply_effect(self.content_package, self.video_file_path, editing_options)
