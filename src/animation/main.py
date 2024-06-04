#!/usr/bin/env python
from crew import NarratedAnimationCrew


def run():
    inputs = {
        "famous_person": "Cristiano Ronaldo",
        "image_folder": "./output/image_generator/",
        "audio_folder": "./output/voice_over_sound/",
        "output_file": "./output/final_video.mp4",
        "inquiry": "I need help to generate a fictional animation video based on the {famous_person} biography. ",
    }
    NarratedAnimationCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
