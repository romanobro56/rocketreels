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
    "coloration": "vibrant",
    "transitions": "shake",
    "transition_duration": 0.3,
    "effects": ["ken_burns"]
  },
  "dark": {
    "zoom": (1, 1.2),
    "coloration": "dark",
    "transitions": "fade",
    "transitions_duration": 0.8,
    "effects": ["ken_burns"]
  },
  "light": {
    "zoom": (1, 1.2),
    "coloration": "light",
    "transitions": "fade",
    "transition_duration": 0.5,
    "effects": ["ken_burns"]
  },
  "default": {
    "zoom": (1, 1.2),
    "coloration": "none",
    "transitions": "fade",
    "transition_duration": 0.5,
    "effects": ["ken_burns"]
  }
}

FONT_SIZES = {
  "extra_small": 1/24,
  "small": 1/22,
  "medium": 1/18,
  "large": 1/14,
  "extra_large": 1/12
}

GRANULARITY_WIDTHS = {
    'small': 0.8,
    'medium': 1.6,
    'large': 2.4
}

SUBTITLE_GRANULARITIES = {
  'word',
  'segment-small',
  'segment-medium',
  'segment-large',
  'sentence'
}