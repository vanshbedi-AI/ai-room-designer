from dotenv import load_dotenv
from openai import OpenAI
from ollama import chat

load_dotenv()


import os

SYSTEM_PROMPT = """
Return ONLY valid JSON.

Use EXACTLY this schema:

{
  "room_type": "string",
  "length": 0,
  "width": 0,
  "height": 9,
  "paint_color": "string",
  "flooring": "string",
  "furniture": [
    {
      "type": "string",
      "count": 1
    }
  ]
}

Rules:
- furniture MUST be a list of objects.
- Never return furniture as strings.
- Every furniture item requires both "type" and "count".
- Combine duplicates into a single object.

Example:

[
  {"type": "floor lamp", "count": 2},
  {"type": "indoor plant", "count": 3}
]

Do not include explanations or markdown.
"""


def get_setting(key: str, default=None):
    return os.getenv(key, default)


USE_OLLAMA = get_setting("USE_OLLAMA", "false").lower() == "true"


def query_ollama(prompt: str):

    response = chat(
        model=get_setting("OLLAMA_MODEL", "qwen2.5:0.5b"),
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
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

    api_key = get_setting("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable is missing."
        )

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
                "content": SYSTEM_PROMPT
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