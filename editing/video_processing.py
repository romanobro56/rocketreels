from moviepy.editor import ImageClip, concatenate_videoclips, vfx
from PIL import Image
class VideoProcessor:

  def create_video_from_images(self, image_path, output_path):
    image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg']  # List of image paths
    clips = [self.ken_burns_effect(img, duration=5) for img in image_paths]  # 5 seconds per image
    video = concatenate_videoclips(clips)
    video.write_videofile("output.mp4", fps=24)

  def ken_burns_effect(self, image_path, duration, start_zoom=1.0, end_zoom=1.2, start_position=(0.5, 0.5), end_position=(0.5, 0.5)):

    clip = ImageClip(image_path, duration=duration)

    start_crop_size = (clip.w / start_zoom, clip.h / start_zoom)
    end_crop_size = (clip.w / end_zoom, clip.h / end_zoom)

    kb_effect = vfx.crop(clip, x_center=clip.w * start_position[0], y_center=clip.h * start_position[1], width=start_crop_size[0], height=start_crop_size[1])
    kb_effect = kb_effect.resize(newsize=(clip.w, clip.h))
    kb_effect = kb_effect.set_position((clip.w * (1 - start_zoom) / 2, clip.h * (1 - start_zoom) / 2))
    kb_effect = kb_effect.crossfadein(0.5)

    return kb_effect.set_duration(duration)