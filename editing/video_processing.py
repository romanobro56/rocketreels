from editing.subtitle_processing import SubtitleProcessor

from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image
import numpy as np
import subprocess
import random
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
      image_file_path = content_package.get_image_file_paths() + f"/dalle_image_{i}.jpg"
      ken_burns_command = self.generate_ken_burns_command(image_file_path, output_path + f"/video_clip{i}.mp4", end-start, i)
      generated_clips.append(output_path+f"/video_clip{i}.mp4")

      subprocess.run(ken_burns_command, shell=True)

    generated_clips = [VideoFileClip(clip) for clip in generated_clips]
    print(generated_clips)

    final_clip = concatenate_videoclips(generated_clips)
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    final_clip.write_videofile(output_path + "/outputFinal.mp4",fps=self.editing_options.get_frame_rate(), codec="libx264", )
    return

  def generate_ken_burns_command(self, image_path, output_path, duration, index):
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
    frames = self.editing_options.get_frame_rate() * duration
    zoom = (self.editing_options.get_zoom()[1] - self.editing_options.get_zoom()[0]) / frames;
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
    zoompan = ""

    match direction:
      case "BR":
        zoompan=f'z=\'zoom+{zoom}\':x=\'{input_width}-{input_width}/zoom\':y=\'{input_height}-{input_height}/zoom\':d={frames}:s={output_width}x{output_height}'
      case "BL":
        zoompan=f'z=\'zoom+{zoom}\':x=\'0\':y=\'{input_width}-{input_height}/zoom\':d={frames}:s={output_width}x{output_height}'
      case "TR":
        zoompan=f'z=\'zoom+{zoom}\':x=\'{input_width}-{input_width}/zoom\':y=\'0\':d={frames}:s={output_width}x{output_height}'
      case "TL":
        zoompan=f'z=\'zoom+{zoom}\':x=\'0\':y=\'0\':d={frames}:s={output_width}x{output_height}'
      case "R":
        zoompan=f'z=\'zoom+{zoom}\':x=\'{input_width}-{input_width}/zoom\':y=\'({input_height}-{output_height}/zoom)/2\':d={frames}:s={output_width}x{output_height}'
      case "L":
        zoompan=f'z=\'zoom+{zoom}\':x=\'0\':y=\'({input_height}-{output_height}/zoom)/2\':d={frames}:s={output_width}x{output_height}'
      case "T":
        zoompan=f'z=\'zoom+{zoom}\':x=\'({input_width}-{output_width}/zoom)/2\':y=\'0\':d={frames}:s={output_width}x{output_height}'
      case "B":
        zoompan=f'z=\'zoom+{zoom}\':x=\'({input_width}-{output_width}/zoom)/2\':y=\'{input_height}-{input_height}/zoom\':d={frames}:s={output_width}x{output_height}'
      case "C":
        zoompan=f'z=\'zoom+{zoom}\':x=\'({input_width}-{output_width}/zoom)/2\':y=\'({input_height}-{output_height}/zoom)/2\':d={frames}:s={output_width}x{output_height}'

    return f'ffmpeg -i {image_path} -filter_complex \"zoompan={zoompan}\" -pix_fmt yuv420p -c:v libx264 -f mp4 {output_path}'