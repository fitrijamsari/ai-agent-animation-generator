import os
from typing import Optional, Type

import requests
from crewai_tools import BaseTool
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# Load the .env file
load_dotenv()

# Set environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()


class Dalle3ImageGeneratorTool(BaseTool):
    name: str = "Dalle3ImageGeneratorTool"
    description: str = "Generates images based on scene descriptions using DALL-E 3."

    def _run(self, scene_description: str, frame_number: int) -> None:
        response = client.images.generate(
            model="dall-e-3",
            prompt=scene_description,
            size="1792x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        directory_path = "./output/image_generator/"
        os.makedirs(directory_path, exist_ok=True)  # Ensure the directory exists

        image_path = os.path.join(
            directory_path, f"image_generation_frame_{frame_number}.jpg"
        )

        # Send a GET request to the image URL
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in write-binary mode and save the image
            with open(image_path, "wb") as file:
                file.write(response.content)
            print(f"Image successfully downloaded: {image_path}")
        else:
            print("Failed to download the image")


if __name__ == "__main__":
    Dalle3ImageGeneratorTool().run(
        scene_description="A young boy named Cesar, around 8 years old, plays soccer on a dusty street in Madeira, Portugal. The background features modest, colorful houses with terracotta roofs and lush, green hillsides. Cristiano, in a worn-out t-shirt and shorts, kicks an old, scuffed soccer ball with great enthusiasm. The scene should capture the innocence and determination of a child with big dreams. The image should have a 16 by 9 aspect ratio with a vibrant 3D Pixar animation style and a cinematic effect. The color scheme should include earthy tones with a touch of vibrant green from the surrounding nature.",
        frame_number=1,
    )

# IDEA 2
# # Define the input schema for the tool
# class DalleInput(BaseModel):
#     prompt: str = Field(description="The prompt for generating the image")
#     frame_number: int = Field(description="The frame number for naming the image")


# class DalleImageGenerator(BaseTool):
#     name = "dalle_image_generator"
#     description = "Generate an image using DALL-E and save it to a directory with a name based on the frame number"
#     args_schema: Type[BaseModel] = DalleInput

#     def _run(
#         self,
#         prompt: str,
#         frame_number: int,
#         run_manager: Optional[CallbackManagerForToolRun] = None,
#     ) -> str:
#         """Use the tool."""
#         api_key = os.getenv("DALL_E_API_KEY")
#         url = "https://api.openai.com/v1/images/generations"

#         headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json",
#         }

#         data = {"model": "dall-e", "prompt": prompt, "num_images": 1}

#         response = requests.post(url, headers=headers, json=data)
#         if response.status_code == 200:
#             image_url = response.json()["data"][0]["url"]
#             image_response = requests.get(image_url)
#             if image_response.status_code == 200:
#                 directory = "generated_images"
#                 os.makedirs(directory, exist_ok=True)
#                 file_path = os.path.join(directory, f"image_{frame_number}.png")
#                 with open(file_path, "wb") as file:
#                     file.write(image_response.content)
#                 return file_path
#             else:
#                 return "Failed to download image"
#         else:
#             return "Failed to generate image"

#     async def _arun(
#         self,
#         prompt: str,
#         frame_number: int,
#         run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
#     ) -> str:
#         """Use the tool asynchronously."""
#         raise NotImplementedError("dalle_image_generator does not support async")


# # Example usage
# dalle_tool = DalleImageGenerator()
# result = dalle_tool._run(prompt="A futuristic cityscape at sunset", frame_number=1)
# print(result)
