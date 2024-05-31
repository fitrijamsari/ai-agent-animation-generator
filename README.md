# AI AGENT FOR ANIMATION GENERATOR

## Introduction

This project is my personal project to generate short animation about any famous biography. The idea is to produce 1 minute duration of animation videos with:

- Just given the name of biographer
- Verification of the script
- Autogenerate animation images
- Autogenerate Voice Over
- Overlayed images, voice over and subtitle

## Technology Used

The following modules are used in this project:

- OpenAI
- LangChain

## Getting started

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
