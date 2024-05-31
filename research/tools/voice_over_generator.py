from crewai_tools import BaseTool
from gtts import gTTS


class VoiceOverTool(BaseTool):
    name: str = "VoiceOverTool"
    description: str = (
        "Generates voice-over from narration script and saves it as an MP3 file."
    )

    def _run(self, narration_script: str, frame_number: int) -> str:
        tts = gTTS(text=narration_script, lang="en")
        file_path = f"../output/voice_over_sound/frame_{frame_number}.mp3"
        tts.save(file_path)
        return f"Voice-over saved as {file_path}"


if __name__ == "__main__":
    VoiceOverTool().run(
        narration_script="On the sidelines of AS Nancy, an animated Wenger passionately directs his players, his early managerial days marked by enthusiasm and dedication. The scene shifts to AS Monaco, where Wenger's strategic brilliance leads the team to a triumphant Ligue 1 title in 1988. Joy and celebration fill the air, with fireworks lighting up Monaco's night sky, capturing the elation of Wenger and his team.",
        frame_number="3",
    )
