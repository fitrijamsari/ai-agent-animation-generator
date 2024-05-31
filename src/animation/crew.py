from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.image_generator import Dalle3ImageGeneratorTool
from tools.search import SearchTools
from tools.voice_over_generator import VoiceOverTool

# Uncomment the following line to use an example of a custom tool
# from instagram.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

# Define tools
image_generator_tool = Dalle3ImageGeneratorTool()
search_internet_tool = SearchTools.search_internet
open_webpage_tool = SearchTools.open_page
voice_over_tool = VoiceOverTool()


@CrewBase
class NarratedAnimationCrew:
    """Narrated Animation crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def scriptwriter(self) -> Agent:
        return Agent(
            config=self.agents_config["scriptwriter"],
            tools=[
                search_internet_tool,
                open_webpage_tool,
            ],
            cache=True,
            verbose=True,
        )

    @agent
    def screenwriter(self) -> Agent:
        return Agent(
            config=self.agents_config["screenwriter"], cache=True, verbose=True
        )

    @agent
    def scene_illustrator(self) -> Agent:
        return Agent(
            config=self.agents_config["scene_illustrator"],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def narrator(self) -> Agent:
        return Agent(config=self.agents_config["narrator"], verbose=True)

    @agent
    def video_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["video_editor"],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def generate_scene_description(self) -> Task:
        return Task(
            config=self.tasks_config["generate_scene_description"],
            agent=self.scriptwriter(),
            output_file="output/scene_description.md",
        )

    @task
    def generate_narration_scripts(self) -> Task:
        return Task(
            config=self.tasks_config["generate_narration_scripts"],
            agent=self.screenwriter(),
            output_file="output/narration_script.md",
        )

    @task
    def generate_frame_images(self) -> Task:
        return Task(
            config=self.tasks_config["generate_frame_images"],
            agent=self.scene_illustrator(),
            output_file="visual-content.md",
        )

    @task
    def generate_voice_over_sound(self) -> Task:
        return Task(
            config=self.tasks_config["generate_voice_over_sound"],
            agent=self.narrator(),
        )

    @task
    def compile_video(self) -> Task:
        return Task(
            config=self.tasks_config["compile_video"],
            agent=self.video_editor(),
            output_file="final-content-strategy.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Narrated Animation Generator crew"""
        return Crew(
            agents=[self.scriptwriter, self.screenwriter],
            tasks=[
                self.generate_scene_description,
                self.generate_narration_scripts,
            ],
            process=Process.sequential,
            verbose=2,
            memory=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    # @crew
    # def crew(self) -> Crew:
    #     """Creates the Narrated Animation Generator crew"""
    #     return Crew(
    #         agents=self.agents,  # Automatically created by the @agent decorator
    #         tasks=self.tasks,  # Automatically created by the @task decorator
    #         process=Process.sequential,
    #         verbose=2,
    #         # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
    #     )
