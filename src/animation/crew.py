import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, SerperDevTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools.image_generator import Dalle3ImageGeneratorTool
from tools.search import SearchTools
from tools.video_compiler import VideoCompilationTool
from tools.voice_over_generator import VoiceOverTool

# Uncomment the following line to use an example of a custom tool
# from instagram.tools.custom_tool import MyCustomTool

# Load the .env file
load_dotenv()

# Set environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

# os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
# os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

# Instantiate tools
search_tool = SerperDevTool()
image_generator_tool = Dalle3ImageGeneratorTool()
search_internet_tool = SearchTools.search_internet
open_webpage_tool = SearchTools.open_page
read_scene_description_tool = FileReadTool(file_path="./output/scene_description.md")
read_narration_script_tool = FileReadTool(file_path="./output/narration_script.md")
voice_over_tool = VoiceOverTool()
video_compiler_tool = VideoCompilationTool()


@CrewBase
class NarratedAnimationCrew:
    """Narrated Animation crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def scriptwriter(self) -> Agent:
        return Agent(
            config=self.agents_config["scriptwriter"],
            tools=[search_tool],
            allow_delegation=True,
            cache=True,
            verbose=True,
            memory=True,
        )

    @agent
    def scene_illustrator(self) -> Agent:
        return Agent(
            config=self.agents_config["scene_illustrator"],
            verbose=True,
            tools=[image_generator_tool],
            allow_delegation=False,
            memory=True,
        )

    @agent
    def screenwriter(self) -> Agent:
        return Agent(
            config=self.agents_config["screenwriter"],
            tools=[],
            cache=True,
            allow_delegation=True,
            verbose=True,
        )

    @agent
    def voice_over_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["voice_over_agent"],
            tools=[voice_over_tool],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def video_compilation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["video_compilation_agent"],
            tools=[video_compiler_tool],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def generate_scene_description(self) -> Task:
        return Task(
            config=self.tasks_config["generate_scene_description"],
            agent=self.scriptwriter(),
            human_input=True,
            output_file="./output/scene_description.md",
        )

    @task
    def generate_frame_images(self) -> Task:
        return Task(
            config=self.tasks_config["generate_frame_images"],
            agent=self.scene_illustrator(),
            # async_execution=True,  # Allow asynchronous execution
        )

    @task
    def generate_narration_scripts(self) -> Task:
        return Task(
            config=self.tasks_config["generate_narration_scripts"],
            agent=self.screenwriter(),
            human_input=True,
            output_file="./output/narration_script.md",
        )

    @task
    def generate_voice_over(self) -> Task:
        return Task(
            config=self.tasks_config["generate_voice_over"],
            agent=self.voice_over_agent(),
            # async_execution=True,  # Allow asynchronous execution
        )

    @task
    def generate_video(self) -> Task:
        return Task(
            config=self.tasks_config["generate_video"],
            agent=self.video_compilation_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Narrated Animation Generator crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            memory=True,
        )

    # @crew
    # def crew(self) -> Crew:
    #     """Creates the Narrated Animation Generator crew"""
    #     return Crew(
    #         agents=self.agents,  # Automatically created by the @agent decorator
    #         tasks=self.tasks,  # Automatically created by the @task decorator
    #         manager_llm=ChatOpenAI(
    #             temperature=0, model="gpt-4o"
    #         ),  # Mandatory for hierarchical process
    #         process=Process.hierarchical,
    #         verbose=2,
    #         memory=True,
    #     )
