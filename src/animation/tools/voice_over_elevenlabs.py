import os

import requests
from crewai_tools import BaseTool
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# Load the .env file
load_dotenv()

# Set environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


class ElevenLabsTool(BaseTool):
    name: str = "ElevenLabs Voice Over Tool"
    description: str = (
        "Generates voice over from text using ElevenLabs API and saves it as an MP3 file."
    )

    def _run(self, text: str, frame_number: int) -> str:
        # Calling the text_to_speech conversion API with detailed parameters
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2",  # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        directory_path = "./output/voice_over_sound/"
        os.makedirs(directory_path, exist_ok=True)  # Ensure the directory exists

        # Generating a unique file name for the output MP3 file
        # save_file_path = f"{uuid.uuid4()}.mp3"
        save_file_path = os.path.join(
            directory_path, f"voice_over_frame_{frame_number}.mp3"
        )

        # Writing the audio to a file
        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"{save_file_path}: A new audio file was saved successfully!")

        # Return the path of the saved audio file
        return save_file_path


if __name__ == "__main__":
    ElevenLabsTool().run(
        text="In a lively neighborhood, young Alejandro dreams big with a tattered ball and boundless spirit. The golden sunset paints his journey of hope and determination.",
        frame_number="4",
    )
