import json
from collections import Counter

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


def extract_room_details(user_prompt: str) -> dict:

    prompt = f"{SYSTEM_PROMPT}\n\nUser Input:\n{user_prompt}"

    response = query_llm(prompt)

    print("RAW MODEL OUTPUT:")
    print(response)

    data = json.loads(response)

    for key, value in DEFAULT_ROOM.items():
        data.setdefault(key, value)

    furniture = data.get("furniture", [])

    if furniture and isinstance(furniture[0], str):

        counts = Counter(furniture)

        data["furniture"] = [
            {"type": item, "count": count}
            for item, count in counts.items()
        ]

    room = RoomRequest(**data)

    return room.model_dump()

    print("RAW RESPONSE:")
    print(data)