from editing.subtitle_processing import SubtitleProcessor

from moviepy.editor import ImageClip, concatenate_videoclips, vfx
from PIL import Image
import numpy as np
import os

class VideoProcessor:
  def __init__(self, editing_options):
    self.editing_options = editing_options
    self.subtitle_processor = SubtitleProcessor()

  def generate_video_from_images(self, content_package, output_path):
    generated_clips = []

    image_timestamps = self.subtitle_processor.get_image_timestamps(content_package.get_subtitles(), content_package.get_transcript_array())
    for i, img_stamp in enumerate(image_timestamps):
      start = img_stamp["start"]
      end = img_stamp["end"]
      image = Image.open(content_package.get_image_file_paths()+f"/dalle_image_{i}.jpg")
      image = image.resize(self.editing_options.get_resolution())
      np_img = np.array(image)

      clip = ImageClip(np_img, duration=end-start)
      generated_clips.append(clip)

    final_clip = concatenate_videoclips(generated_clips)
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    final_clip.write_videofile(output_path + "/output.mp4",fps=self.editing_options.get_frame_rate(), codec="libx264", )
    return
    

  def ken_burns_effect(self, image_path, duration, start_zoom=1.0, end_zoom=1.2, start_position=(0.5, 0.5), end_position=(0.5, 0.5)):

    clip = ImageClip(image_path, duration=duration)

    start_crop_size = (clip.w / start_zoom, clip.h / start_zoom)
    end_crop_size = (clip.w / end_zoom, clip.h / end_zoom)

    kb_effect = vfx.crop(clip, x_center=clip.w * start_position[0], y_center=clip.h * start_position[1], width=start_crop_size[0], height=start_crop_size[1])
    kb_effect = kb_effect.resize(newsize=(clip.w, clip.h))
    kb_effect = kb_effect.set_position((clip.w * (1 - start_zoom) / 2, clip.h * (1 - start_zoom) / 2))
    kb_effect = kb_effect.crossfadein(0.5)

    return kb_effect.set_duration(duration)