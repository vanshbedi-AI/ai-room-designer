import json

from utils.llm_client import query_ollama
from utils.llm_client import query_llm
from shared.schemas import RoomRequest


DEFAULT_ROOM = {
    "room_type": "living room",
    "length": 12,
    "width": 12,
    "height": 9,
    "paint_color": "white",
    "flooring": "wood",
    "furniture": []
}


SYSTEM_PROMPT = """
Return ONLY valid JSON.

Use EXACTLY these keys:

{
  "room_type": "string",
  "length": 0,
  "width": 0,
  "height": 9,
  "paint_color": "string",
  "flooring": "string",
  "furniture": []
}

Do not create nested objects.
Do not rename keys.
Do not include markdown.
Do not include explanations.
"""


def extract_room_details(user_prompt: str) -> dict:

    prompt = f"{SYSTEM_PROMPT}\n\nUser Input:\n{user_prompt}"

    response = query_llm(prompt)

    print("RAW MODEL OUTPUT:")
    print(response)

    data = json.loads(response)

    for key, value in DEFAULT_ROOM.items():
        data.setdefault(key, value)

    room = RoomRequest(**data)

    return room.model_dump()