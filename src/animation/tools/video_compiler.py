import os

from crewai_tools import BaseTool
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

# Load the .env file
load_dotenv()

FFMPEG_EXE_PATH = os.getenv("FFMPEG_EXE_PATH")


class VideoCompilationTool(BaseTool):
    name: str = "VideoCompilationTool"
    description: str = "Compiles images and voice-overs into a single video."

    def _run(self, image_folder: str, audio_folder: str, output_file: str) -> str:
        image_files = sorted(os.listdir(image_folder))
        audio_files = sorted(os.listdir(audio_folder))

        video_clips = []
        for image_file, audio_file in zip(image_files, audio_files):
            if image_file.endswith(".jpg") and audio_file.endswith(".mp3"):
                image_path = os.path.join(image_folder, image_file)
                audio_path = os.path.join(audio_folder, audio_file)

                # Create Image and Audio clips
                image_clip = ImageClip(image_path).set_duration(
                    AudioFileClip(audio_path).duration
                )
                audio_clip = AudioFileClip(audio_path)

                # Set audio for the image clip
                image_clip = image_clip.set_audio(audio_clip)

                video_clips.append(image_clip)

        # Concatenate all video clips
        final_video = concatenate_videoclips(video_clips)

        # Write the final video file
        final_video.write_videofile(
            output_file, codec="libx264", audio_codec="aac", fps=24
        )

        return f"Video compiled and saved as {output_file}"


if __name__ == "__main__":
    VideoCompilationTool().run(
        image_folder="../output/image_generator/",
        audio_folder="../output/voice_over_sound/",
        output_file="../output/final_video.mp4",
    )
