from config.editing_config import RESOLUTIONS, ASPECT_RATIOS, STYLES

class EditingOptions:
  def __init__(self, orientation="vertical", quality="SD", expected_frame_rate=30, ken_burns=True, style="default"):
    self.resolution = RESOLUTIONS[(orientation, quality)]
    self.aspect_ratio = ASPECT_RATIOS[orientation]
    self.frame_rate = expected_frame_rate
    self.expected_horizontal_resolution = self.resolution[0]
    self.expected_vertical_resolution = self.resolution[1]
    self.style = STYLES[style]


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
  
  def get_style(self):
    return self.style
  
  def get_zoom(self):
    return self.style["zoom"]
  
  def get_pan(self):
    return self.style["pan"]
  
  def get_coloration(self):
    return self.style["coloration"]
  
  def get_transitions(self):
    return self.style["transitions"]
  
  def get_transition_duration(self):
    return self.style["transition_duration"]
  
  def get_effects(self):
    return self.style["effects"]
  
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

  def set_style(self, style):
    self.style = STYLES[style]

  def set_zoom(self, zoom):
    self.style["zoom"] = zoom

  def set_pan(self, pan):
    self.style["pan"] = pan

  def set_coloration(self, coloration):
    self.style["coloration"] = coloration

  def set_transitions(self, transitions):
    self.style["transitions"] = transitions

  def set_transition_duration(self, transition_duration):
    self.style["transition_duration"] = transition_duration

  def set_effects(self, effects):
    self.style["effects"] = effects