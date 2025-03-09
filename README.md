# AutoShorts

AutoShorts is an AI-powered video generation pipeline that automatically creates engaging short-form videos (like TikTok, YouTube Shorts, or Instagram Reels) from simple subject inputs. Give it a topic, and it does the rest - generating script, narration, visuals, editing, and subtitles.

## Features

* **Complete Automation** - From idea to finished video with one command
* **AI-Generated Content** - Uses GPT for scripts, DALL-E/Gemini for images, and AI voice synthesis
* **Professional Editing** - Automatic Ken Burns effects, properly timed transitions, and synchronized subtitles
* **Customizable** - Configure resolutions, aspect ratios, fonts, voices, and more
* **Batch Processing** - Generate multiple videos on a subject in parallel

## Demo

<p align="center">

![example](https://github.com/user-attachments/assets/383b7647-37a9-498f-aecf-31833899d64f)


https://github.com/user-attachments/assets/97b3eb25-3dd1-4b0b-8fd2-bc99e17de4ae
</p>

## How It Works

1. **Content Generation** - Creates script/transcript from your topic using GPT
2. **Audio Synthesis** - Converts script to natural-sounding narration using AI voices
3. **Image Generation** - Produces relevant images for each section using DALL-E or Gemini
4. **Video Assembly** - Applies Ken Burns effects to images, synchronizes with audio
5. **Subtitle Integration** - Adds perfectly timed subtitles with customizable styling

## Requirements

- Python 3.12
- FFmpeg
- Pillow/PIL
- libsm6 (for OpenCV support)
- API keys for:
  - OpenAI (required)
  - Google Gemini (optional)
  - ElevenLabs (optional)

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/autoshorts.git
cd autoshorts

# Install dependencies with Poetry
poetry install

# Create config.py with your API keys
cat > config.py << EOF
OPENAI_API_KEY = "your-openai-key"
GEMINI_API_KEY = "your-gemini-key" # Optional
ELEVENLABS_API_KEY = "your-elevenlabs-key" # Optional
EOF
```

## Usage

### Interactive Mode

The easiest way to get started is with the interactive script:

```bash
poetry run python interactive_create_video.py
```

This will guide you through all the options for generating a video.

### Command Line

For more control, use the command-line script:

```bash
poetry run python generate_video.py --subject "History of Pirates" --idea-seed 3 --orientation vertical --quality HD --voice onyx
```

#### Available Options

```
# Content Generation
--subject TEXT           Subject of the video [required]
--idea-seed INTEGER      Idea seed (0-9) [default: 0]
--batch INTEGER          Number of videos to generate in batch [default: 0]
--image-generator TEXT   Image generator to use (openai/gemini) [default: openai]
--tts-provider TEXT      TTS provider to use (openai/elevenlabs) [default: openai]
--voice TEXT             Voice to use for TTS [default: onyx]

# Video Editing
--orientation TEXT       Video orientation (vertical/horizontal/square) [default: vertical]
--quality TEXT           Video quality (HD/4K/8K) [default: HD]
--frame-rate INTEGER     Video frame rate [default: 30]
--font-size TEXT         Font size for subtitles [default: extra_large]
```

### Batch Processing

Generate multiple videos on a topic in one go:

```bash
poetry run python generate_video.py --subject "Space Exploration" --batch 5
```

## Project Structure

- `content_generation_workflow.py` - Main content generation pipeline
- `video_editing_workflow.py` - Video editing and assembly pipeline
- `video_pipeline_workflow.py` - Combines generation and editing processes
- `generation/` - Script, audio, and image generation modules
- `editing/` - Video and subtitle processing modules
- `models/` - Data models and configurations
- `utils/` - Helper utilities
- `editing_config/` - Video editing configurations

## Configuration

Video quality and style settings can be found in `editing_config/editing_config.py`.

The system supports various aspect ratios and quality levels:
- Orientations: vertical (9:16), horizontal (16:9), and square (1:1)
- Quality: HD, 4K, and 8K
- Visual styles: dynamic, dark, light, default

## Credits

This project uses several AI services:
- OpenAI (GPT, Whisper, DALL-E)
- Google Gemini (for image generation)
- ElevenLabs (for voice synthesis)

## License

[MIT License](LICENSE)

## Contributing

Don't you dare try and contribute!

---

<p align="center">
  Made with hate in my heart by <a href="https://github.com/romanobro56">Roman</a>
</p>
