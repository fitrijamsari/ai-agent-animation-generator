import os

from crewai_tools import BaseTool
from gtts import gTTS


class VoiceOverTool(BaseTool):
    name: str = "VoiceOverTool"
    description: str = (
        "Generates voice-over from narration script and saves it as an MP3 file."
    )

    def _run(self, narration_script: str, frame_number: int) -> str:
        directory_path = "./output/voice_over_sound/"
        os.makedirs(directory_path, exist_ok=True)  # Ensure the directory exists

        file_path = os.path.join(directory_path, f"frame_{frame_number}.mp3")
        tts = gTTS(text=narration_script, lang="en")
        tts.save(file_path)
        return f"Voice-over saved as {file_path}"


if __name__ == "__main__":
    VoiceOverTool().run(
        narration_script="On the sidelines of AS Nancy, Wenger's tactical acumen began to shine, marking the start of his remarkable managerial journey.",
        frame_number="4",
    )
