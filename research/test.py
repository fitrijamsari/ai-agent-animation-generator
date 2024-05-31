import os

from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from tools.image_generator import Dalle3ImageGeneratorTool
from tools.search import SearchTools
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
voice_over_tool = VoiceOverTool()


# Define agents
scriptwriter = Agent(
    role="Senior Animation Scriptwriter",
    goal="Generate the scene description for the famous person life story",
    backstory="You are senior animation scriptwriter with a passion for crafting engaging and vivid scene descriptions of the biography of a {famous_person}.",
    tools=[],
    cache=True,
    allow_delegation=False,
    verbose=True,
)

screenwriter = Agent(
    role="Senior Screenwriter",
    goal="Generate narration scripts for each frame based on the scene description",
    backstory="A professional screenwriter with a talent for concise and impactful writing. Your experience in breaking down scenes into detailed scripts ensures each frame is meaningful and engaging.",
    tools=[],
    cache=True,
    allow_delegation=False,
    verbose=True,
)

scene_illustrator = Agent(
    role="Scene Illustrator",
    goal="Generate images for each frame",
    backstory="An experienced artist with a flair for bringing scenes to life through illustrations.",
    tools=[image_generator_tool],
)

voice_over_agent = Agent(
    role="Voice Over Specialist",
    goal="Generate voice-over from provided narration scripts and store them with appropriate frame numbers.",
    backstory=(
        "With a clear and engaging voice, you specialize in transforming written narration into compelling audio, "
        "bringing stories to life with your voice."
    ),
    tools=[voice_over_tool],
    allow_delegation=False,
    verbose=True,
)

video_editor = Agent(
    role="Video Editor",
    goal="Compile the images, voice-over, and subtitles into a video",
    backstory="A skilled video editor with expertise in combining multimedia elements into engaging videos.",
    tools=[],
)

# Define tasks
generate_scene_description = Task(
    description="Conduct an in-depth biography analysis of {famous_person}. Utilize all available data sources to compile a detailed profile, focusing on the live story, major achievement and contribution.  "
    "This facts is crucial. Don't make assumptions and only use information you absolutely sure about.",
    expected_output="Produce 6 frames of comprehensive scene description that will be used as a prompt for dalle 3 image generator of the {famous_person} life story. It should be covering the key facts, major achievement and contribution.  "
    "Write each scene description as detail as possible with a specific setting. For instance, 'a medieval knight standing guard outside a stone castle covered in ivy.'  "
    "The scene description shall be descriptive. For example, Instead of saying 'a cat,' you might say 'a photograph of a fluffy orange cat with green eyes sitting on a windowsill at sunset.'  "
    "The image type should be like manga animation style. If you have a specific color scheme in mind, mention it for example 'A tranquil beach scene dominated by shades of turquoise, gold, and coral pink.'  ",
    agent=scriptwriter,
    output_file="output/scene_description.md",
)

generate_narration_scripts = Task(
    description="Create voice over scripts for each frame based on the scene description.",
    expected_output="Voice over scripts for each frame as third person view. The script should be about 5-6 seconds duration per frame.  "
    "Ensure the tone is enthusiastic, professional, and aligned with animation identity. ",
    agent=screenwriter,
    output_file="output/narration_script.md",
)

generate_frame_images = Task(
    description="Generate images for each frame based on the frame scripts.",
    expected_output="Illustrations for each frame.",
    agent=scene_illustrator,
)

generate_voice_over = Task(
    description=(
        "Generate a voice-over for the following narration script. "
        "Save the voice-over with the filename based on the frame number."
    ),
    expected_output="An MP3 file saved with the frame number as the filename.",
    tools=[voice_over_tool],
    agent=voice_over_agent,
)


compile_video = Task(
    description="Compile the images, voice-over, and subtitles into a video.",
    expected_output="A final video file.",
    agent=video_editor,
)

user_confirmation_task = Task(
    description="Confirm each generated output with the user before proceeding.",
    expected_output="User confirmation for each step.",
    agent=None,  # This is a manual step requiring user interaction
)

# Form the crew
crew = Crew(
    agents=[scriptwriter, screenwriter, voice_over_agent],
    tasks=[generate_scene_description, generate_narration_scripts, generate_voice_over],
    process=Process.sequential,
    memory=True,
    verbose=2,
)

inputs = {
    "famous_person": "Arsene Wenger",
    "inquiry": "I need help to generate a 1 minute animation video based on the {famous_person} biography. ",
}
result = crew.kickoff(inputs=inputs)
