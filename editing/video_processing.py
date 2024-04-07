from editing.subtitle_processing import SubtitleProcessor

from moviepy.editor import ImageClip, concatenate_videoclips, vfx
from PIL import Image
import numpy as np
import subprocess
import random
import os

class VideoProcessor:
  def __init__(self, editing_options):
    self.editing_options = editing_options
    self.subtitle_processor = SubtitleProcessor()

  # def generate_video_from_images(self, content_package, output_path):
  #   generated_clips = []

  #   image_timestamps = self.subtitle_processor.get_image_timestamps(content_package.get_subtitles(), content_package.get_transcript_array())
  #   for i, img_stamp in enumerate(image_timestamps):
  #     start = img_stamp["start"]
  #     end = img_stamp["end"]
  #     image = Image.open(content_package.get_image_file_paths()+f"/dalle_image_{i}.jpg")
  #     image = image.resize(self.editing_options.get_resolution())
  #     np_img = np.array(image)

  #     clip = ImageClip(np_img, duration=end-start)
  #     generated_clips.append(clip)

  #   final_clip = concatenate_videoclips(generated_clips)
  #   if not os.path.exists(output_path):
  #     os.makedirs(output_path)
  #   final_clip.write_videofile(output_path + "/output.mp4",fps=self.editing_options.get_frame_rate(), codec="libx264", )
  #   return

  def generate_video_from_images(self, content_package, output_path):
    subtitles = content_package.get_subtitles()
    image_timestamps = self.subtitle_processor.get_image_timestamps(subtitles, content_package.get_transcript_array())


  def generate_ken_burns_command(self, image_path, output_video_path, duration):
    """
    example zoom pan / pad command
    pad=
      w=9600:h=6000:
      x='(ow-iw)/2':y='(oh-ih)/2',
    zoompan=
      x='(iw-0.625*ih)/2':
      y='(1-on/(25*4))*(ih-ih/zoom)':
      z='if(eq(on,1),2.56,zoom+0.002)':
      d=25*4:s=1280x800
    """
    output_width = self.editing_options.get_resolution()[0]
    output_height = self.editing_options.get_resolution()[1]
    zoom = self.editing_options.get_zoom()
    frames = self.editing_options.get_frame_rate() * duration
    input_width = Image.open(image_path).size[0]
    input_height = Image.open(image_path).size[1]

    if input_width / input_height > output_width / output_height:
      possible_directions = ["R", "L", "C"]
      if input_width/input_height - output_width/ output_height <= 3/4:
        possible_directions.extend(["TR", "TL", "BR", "BL"])

    elif input_width / input_height < output_width / output_height:
      possible_directions = ["T", "B" "C"]
      if input_width / input_height - output_width / output_height >= -3/4:
        possible_directions.extend(["TR", "TL", "BR", "BL"])
    else:
      possible_directions = ["R", "L", "T", "B", "C", "TR", "TL", "BR", "BL"]

    direction = random.choice(possible_directions)

    match direction:
      case "R":
        pass
      case "L":
        pass
      case "T":
        pass
      case "B":
        pass
      case "C":
        pass
      case "TR":
        pass
      case "TL":
        pass
      case "BR":
        pass
      case "BL":
        pass



    return f"ffmpeg -loop 1 -i {image_path} -vf \"zoompan=z='{zoom[0]}':d=125:x='{pan[0] * resolution[0]}':y='{pan[1] * resolution[1]}'\" -t 5 -s {resolution[0]}x{resolution[1]} {output_video_path}"


    

  def ken_burns_effect(self, image_path, duration, start_zoom=1.0, end_zoom=1.2, start_position=(0.5, 0.5), end_position=(0.5, 0.5)):

    clip = ImageClip(image_path, duration=duration)

    start_crop_size = (clip.w / start_zoom, clip.h / start_zoom)
    end_crop_size = (clip.w / end_zoom, clip.h / end_zoom)

    kb_effect = vfx.crop(clip, x_center=clip.w * start_position[0], y_center=clip.h * start_position[1], width=start_crop_size[0], height=start_crop_size[1])
    kb_effect = kb_effect.resize(newsize=(clip.w, clip.h))
    kb_effect = kb_effect.set_position((clip.w * (1 - start_zoom) / 2, clip.h * (1 - start_zoom) / 2))
    kb_effect = kb_effect.crossfadein(0.5)

    return kb_effect.set_duration(duration)
  

  def create_zoom_effect(input_image, output_video):
    command = [
      'ffmpeg', '-i', input_image,
      '-filter_complex', "zoompan=z='zoom+0.002':d=25*4:s=1280x800",
      '-pix_fmt', 'yuv420p', '-c:v', 'libx264', output_video
    ]
    
    try:
      # Execute the FFmpeg command
      subprocess.run(command, check=True)
      print(f"Zoom effect applied successfully: {output_video}")
    except subprocess.CalledProcessError as e:
      # Handle errors during the process
      print(f"Error applying zoom effect: {e}")