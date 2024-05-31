# AI AGENT FOR ANIMATION GENERATOR

## INTRODUCTION

This project is my personal project to generate short animation about any famous biography using crewai. The idea is to produce 1 minute duration of animation videos with the following workflow:

## THE WORKFLOW

### 1. Input Handling:

User Input: Take the name of a famous person from the user.

### 2. Scene Description Generation:

Agent: Scriptwriter  
Task: Generate the overall scene description based on the given person.

### 3. Script Generation:

Agent: Screenwriter  
Task: Generate a script for each frame (5-6 seconds per frame).

### 4. Image Generation:

Agent: Scene Illustrator  
Task: Generate images for each frame based on the scene descriptions.

### 5. Voice Over Script Generation:

Agent: Narrator  
Task: Generate the voice-over script for each frame.

### 6. Compile Video:

Agent: Video Editor  
Task: Compile the images, voice-over, and subtitles into a video.

### 7. User Confirmation:

Process: After each task, get user confirmation before proceeding to the next task.

## AGENTS & TASKS

### Agents

#### 1. Scriptwriter

Role: Generate the overall scene description.  
Goal: Create a vivid and engaging scene description based on the famous person.  
Backstory: A creative mind with a knack for crafting engaging and vivid scene descriptions.  
Tools: LLM tool for generating descriptions.

#### 2. Screenwriter

Role: Generate scripts for each frame.  
Goal: Break down the overall scene description into detailed scripts for each frame.  
Backstory: A professional screenwriter with a talent for concise and impactful writing.  
Tools: LLM tool for script generation.

#### 3. Scene Illustrator

Role: Generate images for each frame.  
Goal: Create detailed illustrations based on the scene descriptions.  
Backstory: An experienced artist with a flair for bringing scenes to life through illustrations.  
Tools: DALL-E or a similar image generation tool.

#### 4. Narrator

Role: Generate voice-over scripts for each frame.  
Goal: Create engaging voice-over scripts that align with the scene descriptions and scripts.  
Backstory: A professional narrator with a clear and engaging voice.  
Tools: LLM tool for script generation.

#### 5.Video Editor

Role: Compile the images, voice-over, and subtitles into a video.  
Goal: Create a cohesive video from the generated assets.  
Backstory: A skilled video editor with expertise in combining multimedia elements into engaging videos.  
Tools: FFmpeg or a similar video editing tool.

### Tasks

#### 1. Generate Scene Description

Description: Generate an overall scene description for the famous person.  
Expected Output: A comprehensive scene description.  
Tools: LLM tool.  
Agent: Scriptwriter.

#### 2.Generate Frame Scripts

Description: Create scripts for each frame based on the scene description.  
Expected Output: Scripts for each frame (5-6 seconds per frame).  
Tools: LLM tool.  
Agent: Screenwriter.

#### 3. Generate Frame Images

Description: Generate images for each frame based on the frame scripts.  
Expected Output: Illustrations for each frame.  
Tools: DALL-E or a similar image generation tool.  
Agent: Scene Illustrator.

#### 4. Generate Voice Over Scripts

Description: Create voice-over scripts for each frame.  
Expected Output: Voice-over scripts for each frame.  
Tools: LLM tool.  
Agent: Narrator.

#### 5. User Confirmation

Description: Confirm each generated output with the user before proceeding.  
Expected Output: User confirmation for each step.

#### 6. Compile Video

Description: Compile the images, voice-over, and subtitles into a video.  
Expected Output: A final video file.  
Tools: FFmpeg or a similar video editing tool.  
Agent: Video Editor.

## TECHNOLOGY USED

The following modules are used in this project:

- OpenAI
- CrewAI
- LangChain

## GETTING STARTED

To run this demo project, create an virtual environment and install the src package:

1. Clone the repository:

2. create .env files with the following secret keys:

```bash
LANGCHAIN_TRACING_V2='true'
LANGCHAIN_ENDPOINT='https://api.smith.langchain.com'
LANGCHAIN_API_KEY=<your-api-key>

OPENAI_API_KEY=<your-api-key>
GROQ_API_KEY=<your-api-key>
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
streamlit run src/app.py
```

## Challenges

1.

## To Do

1.

## Reference & Documentation

1. [LangChain with SQL Documentation](https://python.langchain.com/docs/use_cases/sql/quickstart/)
2. [Streamlit Documentation](https://docs.streamlit.io/get-started/tutorials/create-an-app)
