from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "output_text_to_speech.flac"
response = client.audio.speech.create(
  model="tts-1",
  voice="nova",
  input="Today is a wonderful day to build something people love!,才兵，你在摸鱼？"
)

response.stream_to_file(speech_file_path)