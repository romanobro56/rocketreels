from editing_config.editing_config import ( 
  RESOLUTIONS, 
  ASPECT_RATIOS, 
  STYLES, 
  FONT_SIZES,
  GRANULARITY_WIDTHS,
)

class EditingOptions:
  def __init__(
    self, 
    orientation="vertical", 
    quality="HD", 
    expected_frame_rate=30, 
    ken_burns=True, 
    style="default", 
    font_family='Titan-One',
    font_size="medium",
    subtitle_granularity_width = 'medium'
  ):
    self.resolution = RESOLUTIONS[(orientation, quality)]
    self.aspect_ratio = ASPECT_RATIOS[orientation]
    self.frame_rate = expected_frame_rate
    self.ken_burns = ken_burns
    self.style = STYLES[style]
    self.font_family=font_family
    self.font_size=FONT_SIZES[font_size]
    self.subtitle_granularity_width = GRANULARITY_WIDTHS[subtitle_granularity_width]

  def get_resolution(self):
    return self.resolution
  
  def get_frame_rate(self):
    return self.frame_rate
  
  def get_zoom(self):
    return self.style["zoom"]

  def get_horizontal_resolution(self):
    return self.resolution[0]
  
  def get_vertical_resolution(self):
    return self.resolution[1]
  
  def get_font_family(self):
    return self.font_family
  
  def get_font_size(self):
    return self.font_size * self.resolution[0]
  
  def get_subtitle_granularity_width(self):
    return self.subtitle_granularity_width