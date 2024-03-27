class EditingOptions:
  RESOLUTIONS = {
    ("vertical", "SD"): (1080, 1920),
    ("vertical", "HD"): (2160, 3840),
    ("horizontal", "SD"): (1920, 1080),
    ("horizontal", "HD"): (3840, 2160),
    ("square", "SD"): (1080, 1080),
    ("square", "HD"): (2160, 2160)
  }
  
  ASPECT_RATIOS = {
    "vertical": 9/16,
    "horizontal": 16/9,
    "square": 1/1
  }

  def __init__(self, orientation="vertical", quality="SD", expected_frame_rate=30):
    self.expected_horizontal_resolution, self.expected_vertical_resolution = self.RESOLUTIONS[(orientation, quality)]
    self.expected_aspect_ratio = self.ASPECT_RATIOS[orientation]

    self.frame_rate = expected_frame_rate

  ### GETTERS ###

  def get_resolution(self):
    return self.resolution

  def get_frame_rate(self):
    return self.frame_rate

  def get_aspect_ratio(self):
    return self.aspect_ratio

  def get_expected_horizontal_resolution(self):
    return self.expected_horizontal_resolution

  def get_expected_vertical_resolution(self):
    return self.expected_vertical_resolution

  def get_expected_aspect_ratio(self):
    return self.expected_aspect_ratio
  
  ### SETTERS ###

  def set_resolution(self, resolution):
    self.resolution = resolution

  def set_frame_rate(self, frame_rate):
    self.frame_rate = frame_rate

  def set_aspect_ratio(self, aspect_ratio):
    self.aspect_ratio = aspect_ratio

  def set_expected_horizontal_resolution(self, horizontal_resolution):
    self.expected_horizontal_resolution = horizontal_resolution

  def set_expected_vertical_resolution(self, vertical_resolution):
    self.expected_vertical_resolution = vertical_resolution

  def set_expected_aspect_ratio(self, expected_aspect_ratio):
    self.expected_aspect_ratio = expected_aspect_ratio

