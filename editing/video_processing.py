from editing.subtitle_processing import SubtitleProcessor 
from utils.utilities import write_string_to_file

from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.VideoClip import TextClip
from PIL import Image, ImageFont
import numpy as np
import subprocess
import textwrap
import random
import os

class VideoProcessor:
  def __init__(self, editing_options):
    self.editing_options = editing_options
    self.subtitle_processor = SubtitleProcessor()

  def generate_video_from_images(self, content_package, output_path):
    generated_clip_files = []

    image_timestamps = self.subtitle_processor.get_image_timestamps(content_package.get_subtitles(), content_package.get_transcript_array())
    for i, img_stamp in enumerate(image_timestamps):
      start = img_stamp["start"]
      end = img_stamp["end"]
      image_file_path = content_package.get_image_file_paths() + f"/dalle_image_{i}.jpg"
      ken_burns_command = self.generate_ken_burns_command(image_file_path, output_path + f"/video_clip{i}.mp4", end-start, i)
      generated_clip_files.append(output_path+f"/video_clip{i}.mp4")

      subprocess.run(ken_burns_command, shell=True)

    generated_clips = [VideoFileClip(file) for file in generated_clip_files]

    for file in generated_clip_files:
      os.remove(file)

    final_clip = concatenate_videoclips(generated_clips)
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    final_clip.write_videofile(output_path + "/outputSilent.mp4",fps=self.editing_options.get_frame_rate(), codec="libx264")
    return (output_path + "/outputSilent.mp4")

  def generate_ken_burns_command(self, image_path, output_path, duration, index):
    """
    Enhanced Ken Burns effect with proper aspect ratio handling through center cropping
    """
    output_width = self.editing_options.get_resolution()[0]
    output_height = self.editing_options.get_resolution()[1]
    output_aspect_ratio = output_width / output_height
    frame_rate = self.editing_options.get_frame_rate()
    frames = int(frame_rate * duration)
    
    # Get image dimensions
    img = Image.open(image_path)
    img_width, img_height = img.size
    img_aspect_ratio = img_width / img_height
    
    # Calculate upscale factor
    upscale_factor = 4
    
    # High-res dimensions
    high_res_width = output_width * upscale_factor
    high_res_height = output_height * upscale_factor
    
    # Zoom settings
    zoom_min, zoom_max = self.editing_options.get_zoom()
    zoom_min = max(1.0, zoom_min)
    zoom_max = min(1.5, zoom_max)
    
    # Seed random
    random.seed(index)
    effect = random.choice(["zoom_in", "zoom_out"])
    
    # Build filters
    filters = []
    
    # First, scale the image to maintain aspect ratio while ensuring
    # it's large enough for the target dimensions
    if img_aspect_ratio > output_aspect_ratio:
        # Image is wider: scale to height and crop width
        scaled_height = high_res_height
        scaled_width = int(scaled_height * img_aspect_ratio)
    else:
        # Image is taller: scale to width and crop height
        scaled_width = high_res_width
        scaled_height = int(scaled_width / img_aspect_ratio)
    
    filters.append(f"scale={scaled_width}:{scaled_height}:flags=lanczos")
    
    # Crop to target aspect ratio (center crop)
    if img_aspect_ratio != output_aspect_ratio:
        if img_aspect_ratio > output_aspect_ratio:
            # Crop width
            crop_width = int(scaled_height * output_aspect_ratio)
            crop_height = scaled_height
            crop_x = (scaled_width - crop_width) // 2
            crop_y = 0
        else:
            # Crop height
            crop_width = scaled_width
            crop_height = int(scaled_width / output_aspect_ratio)
            crop_x = 0
            crop_y = (scaled_height - crop_height) // 2
        
        filters.append(f"crop={crop_width}:{crop_height}:{crop_x}:{crop_y}")
    
    # Apply zoompan effect
    if effect == "zoom_in":
        filters.append(
            f"zoompan="
            f"z='min({zoom_max},{zoom_min}+({zoom_max}-{zoom_min})*on/{frames})':"
            f"x='(iw-iw/zoom)/2':"
            f"y='(ih-ih/zoom)/2':"
            f"d={frames}:s={high_res_width}x{high_res_height}"
        )
    else:  # zoom_out
        filters.append(
            f"zoompan="
            f"z='max({zoom_min},{zoom_max}-({zoom_max}-{zoom_min})*on/{frames})':"
            f"x='(iw-iw/zoom)/2':"
            f"y='(ih-ih/zoom)/2':"
            f"d={frames}:s={high_res_width}x{high_res_height}"
        )
    
    # Final downscale
    filters.append(f"scale={output_width}:{output_height}:flags=lanczos")
    
    # Ensure proper format
    filters.append("format=yuv420p")
    
    # Join filters
    filter_string = ",".join(filters)
    
    command = (
        f'ffmpeg -y -i {image_path} '
        f'-vf "{filter_string}" '
        f'-c:v libx264 -preset medium -pix_fmt yuv420p -r {frame_rate} '
        f'-t {duration} {output_path}'
    )
    
    return command

  def overlay_audio(self, content_package, video_file_clip, video_file_path):
    audioclip = AudioFileClip(video_file_path + "/audio/audio.mp3")

    audio_video_clip = video_file_clip.set_audio(audioclip)
    audio_video_clip.write_videofile(
        video_file_path + "/output.mp4",
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k"
    )

  def generate_color_block(self, txt, width, font_size):
    font = ImageFont.truetype(self.editing_options.get_font_family(), font_size)
    ascent, descent = font.getmetrics()
    line_height = ascent + descent + 4
    width = font.getlength('')
    wrapped_lines = textwrap.wrap(txt, width=estimate_chars_per_line(font_size, width))
    num_lines = len(wrapped_lines)

    block_height = font_size + 2 * 10
    block_width = width * .82
    block = np.zeros((int(block_height), int(block_width), 4), dtype=np.uint8)
    block[:, :, :3] = (0,0,0)
    block[:, :, 3] = 128
    color_block = ImageClip(block).set_position(("center","center"))

    return (subtitles, color_block)
  
  def overlay_subtitles(self, content_package, video_file_clip, output_path):
    width = self.editing_options.get_horizontal_resolution()
    height = self.editing_options.get_vertical_resolution()
    font_pt_size = self.editing_options.get_font_size()

    subtitles = content_package.get_subtitles()
    subtitles = self.subtitle_processor.set_sub_granularity_json(subtitles, self.editing_options)
    content_package.set_subtitles(subtitles)
    srt_subtitles = self.subtitle_processor.json_to_srt(content_package.get_subtitles())
    print(subtitles)
    write_string_to_file(srt_subtitles, output_path + "/audio/subtitles.srt")

    generator = lambda txt: TextClip(
      txt,
      font=self.editing_options.get_font_family(),
      fontsize=font_pt_size,
      stroke_width=self.editing_options.get_font_stroke_width(), 
      color='white', 
      stroke_color=self.editing_options.get_font_stroke_color(), 
      size=( width * .8, height), 
      method='caption',
      align='center'
    )

    subtitles = SubtitlesClip(output_path + "/audio/subtitles.srt", generator)

    final = CompositeVideoClip([video_file_clip, subtitles.set_position(('center', 'center'))])
    subtitled_video_path = output_path + "/outputSubtitled.mp4"
    final.write_videofile(subtitled_video_path, self.editing_options.get_frame_rate())