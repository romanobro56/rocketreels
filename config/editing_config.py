RESOLUTIONS = {
  ("vertical", "HD"): (1080, 1920),
  ("vertical", "4K"): (2160, 3840),
  ("vertical", "8K"): (4320, 7680),
  ("horizontal", "HD"): (1920, 1080),
  ("horizontal", "4K"): (3840, 2160),
  ("horizontal", "8K"): (7680, 4320),
  ("square", "HD"): (1080, 1080),
  ("square", "4K"): (2160, 2160),
  ("square", "8K"): (4320, 4320)
}

ASPECT_RATIOS = {
  "vertical": 9/16,
  "horizontal": 16/9,
  "square": 1/1
}

STYLES = {
  "dynamic" : {
    "zoom": (1.2, 2),
    "pan": (0.2, 0.8),
    "coloration": "vibrant",
    "transitions": "shake",
    "transition_duration": 0.3,
    "effects": ["ken_burns"]
  },
  "dark": {
    "zoom": (1, 1.2),
    "pan": (0.2, 0.6),
    "coloration": "dark",
    "transitions": "fade",
    "transitions_duration": 0.8,
    "effects": ["ken_burns"]
  },
  "light": {
    "zoom": (1, 1.2),
    "pan": (0.2, 0.6),
    "coloration": "light",
    "transitions": "fade",
    "transition_duration": 0.5,
    "effects": ["ken_burns"]
  },
  "default": {
    "zoom": (1, 1.2),
    "pan": (0.2, 0.6),
    "coloration": "none",
    "transitions": "fade",
    "transition_duration": 0.5,
    "effects": ["ken_burns"]
  }
}
