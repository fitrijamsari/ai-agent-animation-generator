#!/usr/bin/env python
import datetime

from crew import NarratedAnimationCrew


def run():
    inputs = {
        "famous_person": input(
            "Enter the any famous person name you want to generate a video here: "
        ),
        "inquiry": "I need help to generate a 1 minute animation video based on the {famous_person} biography. ",
    }
    NarratedAnimationCrew().crew().kickoff(inputs=inputs)
