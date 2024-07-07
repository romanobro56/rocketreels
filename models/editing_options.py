from editing_config.editing_config import RESOLUTIONS, ASPECT_RATIOS, STYLES

class EditingOptions:
  def __init__(self, orientation="vertical", quality="SD", expected_frame_rate=30, ken_burns=True, style="default"):
    self.resolution = RESOLUTIONS[(orientation, quality)]
    self.aspect_ratio = ASPECT_RATIOS[orientation]
    self.frame_rate = expected_frame_rate
    self.expected_horizontal_resolution = self.resolution[0]
    self.expected_vertical_resolution = self.resolution[1]
    self.style = STYLES[style]

  def get_resolution(self):
    return self.resolution
  
  def get_frame_rate(self):
    return self.frame_rate
  
  def get_zoom(self):
    return self.style["zoom"]
