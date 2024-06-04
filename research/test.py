import os

from crewai import Agent, Crew, Process, Task
from crewai_tools import FileReadTool, SerperDevTool
from dotenv import load_dotenv
from tools.image_generator import Dalle3ImageGeneratorTool
from tools.search import SearchTools
from tools.video_compiler import VideoCompilationTool
from tools.voice_over_generator import VoiceOverTool

# Load the .env file
load_dotenv()

# Set environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
DALLE_API_KEY = os.getenv("DALLE_API_KEY")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")

# os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

# Instantiate tools
search_tool = SerperDevTool()
image_generator_tool = Dalle3ImageGeneratorTool()
search_internet_tool = SearchTools.search_internet
open_webpage_tool = SearchTools.open_page
read_scene_description_tool = FileReadTool(file_path=".output/scene_description.md")
voice_over_tool = VoiceOverTool()
video_compiler_tool = VideoCompilationTool()


# Define agents
scriptwriter = Agent(
    role="Senior Animation Scriptwriter",
    goal="Generate the scene description for a short animated video based on the {famous_person} life story",
    backstory="You are senior animation scriptwriter with a passion for crafting engaging and vivid scene descriptions of the biography of a {famous_person}.",
    tools=[],
    cache=True,
    allow_delegation=True,
    verbose=True,
)

screenwriter = Agent(
    role="Senior Screenwriter",
    goal="Generate narration scripts for each frame based on the scene description",
    backstory="A professional screenwriter with a talent for concise and impactful writing. Your experience in breaking down scenes into detailed scripts ensures each frame is meaningful and engaging.",
    tools=[],
    cache=True,
    allow_delegation=True,
    verbose=True,
)

scene_illustrator = Agent(
    role="Scene Illustrator",
    goal="Generate images for each frame based on the scene description produced by scriptwriter and store them with respective frame numbers",
    backstory="An experienced artist with a flair for bringing scenes to life through illustrations.",
    tools=[image_generator_tool],
    allow_delegation=False,
)

voice_over_agent = Agent(
    role="Voice Over Specialist",
    goal="Generate voice-over from provided narration scripts produced by screenwriter and store them with respective frame numbers.",
    backstory=(
        "With a clear and engaging voice, you specialize in transforming written narration into compelling audio, "
        "bringing stories to life with your voice."
    ),
    tools=[voice_over_tool],
    allow_delegation=False,
    verbose=True,
)

video_compilation_agent = Agent(
    role="Video Compilation Specialist",
    goal="Compile images and voice-overs into a single video.",
    backstory=(
        "With a knack for storytelling through visuals and audio, you specialize in creating seamless video experiences, "
        "bringing together images and sound to create engaging content."
    ),
    tools=[video_compiler_tool],
    allow_delegation=True,
    verbose=True,
)

# Define tasks
generate_scene_description = Task(
    description="Conduct an in-depth biography analysis of {famous_person}. Utilize all available data sources to compile a detailed profile, focusing on the live story, major achievement and contribution.  "
    "This facts is crucial. Don't make assumptions and only use information you absolutely sure about.",
    expected_output="Produce 3 frames of comprehensive scene description that will be used as a prompt for dalle 3 image generator of the {famous_person} life story. However, replace the {famous_person} name with a fictional name. If there are any specific branding elements or trademarked words in the scene, replace them with general description, for example if there are words like Manchester United, Manchester City, Arsenal, Real Madrid, etc. you can replace with 'football club'.  "
    "The life story should be covering the key facts, major achievement and contribution.  "
    "Write each scene description as detail as possible with a specific setting. For instance, 'a medieval knight standing guard outside a stone castle covered in ivy.'  "
    "The scene description shall be descriptive. For example, Instead of saying 'a cat,' you might say 'a photograph of a fluffy orange cat with green eyes sitting on a windowsill at sunset.'  "
    "Mention in each scene description that the image should have a size of 1792x1024 with a vibrant cartoon 3D Pixar animation style and a cinematic effect.  "
    "If you have a specific color scheme in mind, mention it for example 'A tranquil beach scene dominated by shades of turquoise, gold, and coral pink.'  ",
    human_input=True,
    agent=scriptwriter,
    output_file="./output/scene_description.md",
)

generate_narration_scripts = Task(
    description="Create voice over scripts for each frame based on the scene description.",
    expected_output="From the scene description, generate voice over scripts or narration for each frame as third person view. The script should be about 5-6 seconds duration per frame.  "
    "Ensure the tone is enthusiastic, professional, and aligned with animation identity. ",
    human_input=True,
    agent=screenwriter,
    output_file="./output/narration_script.md",
)

generate_frame_images = Task(
    description="Generate images for each frame based on the screen description produced by scriptwriter.",
    expected_output="Generate images based on the screen description produced by the scriptwriter for each frame. Each images shall be stored in {image_folder}.  ",
    agent=scene_illustrator,
)

generate_voice_over = Task(
    description=(
        "Generate a voice-over for the following narration script for each frame. "
        "Save the voice-over with the filename based on the frame number."
    ),
    expected_output="Generate voice-over sound based on the screen description produced by the scriptwriter for each frame. Each sound shall be stored in {image_folder} and MP3 format. ",
    agent=voice_over_agent,
)


generate_video = Task(
    description=(
        "Generate a video with generated images and voice-overs of respective frames.  "
    ),
    expected_output="Compile generated images from the folder {image_folder} and with the respective voice-overs of each frame from the folder {audio_folder} into a single video. "
    "Save the video as {output_file}.  ",
    agent=video_compilation_agent,
)


# Form the crew
crew = Crew(
    agents=[
        scriptwriter,
        screenwriter,
        scene_illustrator,
        voice_over_agent,
        video_compilation_agent,
    ],
    tasks=[
        generate_scene_description,
        generate_narration_scripts,
        generate_frame_images,
        generate_voice_over,
        generate_video,
    ],
    process=Process.sequential,
    memory=True,
    verbose=2,
)

inputs = {
    "famous_person": "Brad Pit",
    "image_folder": "./output/image_generator/",
    "audio_folder": "./output/voice_over_sound/",
    "output_file": "./output/final_video.mp4",
    "inquiry": "I need help to generate a fictional animation video based on the {famous_person} biography. ",
}
result = crew.kickoff(inputs=inputs)
