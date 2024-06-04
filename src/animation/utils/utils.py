# Add your utilities or helper functions to this file.

import os

import tiktoken
from dotenv import find_dotenv, load_dotenv


def load_env():
    _ = load_dotenv(find_dotenv())


def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


def get_serper_api_key():
    load_env()
    openai_api_key = os.getenv("SERPER_API_KEY")
    return openai_api_key


def count_tokens(input_string: str) -> int:
    tokenizer = tiktoken.get_encoding("cl100k_base")

    tokens = tokenizer.encode(input_string)

    return len(tokens)


def calculate_cost(input_string: str, cost_per_million_tokens: float = 5) -> float:
    num_tokens = count_tokens(input_string)

    total_cost = (num_tokens / 1_000_000) * cost_per_million_tokens

    return total_cost


# break line every 80 characters if line is longer than 80 characters
# don't break in the middle of a word
def pretty_print_result(result):
    parsed_result = []
    for line in result.split("\n"):
        if len(line) > 80:
            words = line.split(" ")
            new_line = ""
            for word in words:
                if len(new_line) + len(word) + 1 > 80:
                    parsed_result.append(new_line)
                    new_line = word
                else:
                    if new_line == "":
                        new_line = word
                    else:
                        new_line += " " + word
            parsed_result.append(new_line)
        else:
            parsed_result.append(line)
    return "\n".join(parsed_result)
