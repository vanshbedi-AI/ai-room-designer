import os

from dotenv import load_dotenv
from openai import OpenAI
from ollama import chat

load_dotenv()


def get_setting(key: str, default=None):
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)


USE_OLLAMA = get_setting("USE_OLLAMA", "false").lower() == "true"


def query_ollama(prompt: str):

    response = chat(
        model=get_setting("OLLAMA_MODEL", "qwen2.5:0.5b"),
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    return response.message.content


def query_groq(prompt: str):

    client = OpenAI(
        api_key=get_setting("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model=get_setting(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        ),
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def query_llm(prompt: str):

    if USE_OLLAMA:
        return query_ollama(prompt)

    return query_groq(prompt)