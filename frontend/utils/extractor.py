import json
from collections import Counter

from shared.schemas import RoomRequest
from utils.llm_client import query_llm


DEFAULT_ROOM = {
    "room_type": "living room",
    "length": 12,
    "width": 12,
    "height": 9,
    "paint_color": "white",
    "flooring": "wood",
    "furniture": []
}


def normalize_furniture(furniture):

    if not furniture:
        return []

    # Model returned:
    # ["bed", "table", "table"]

    if isinstance(furniture[0], str):

        counts = Counter(furniture)

        return [
            {
                "type": item,
                "count": count
            }
            for item, count in counts.items()
        ]

    # Model already returned correct format
    return furniture


def extract_room_details(user_prompt: str):

    response = query_llm(user_prompt)

    data = json.loads(response)

    print("RAW LLM OUTPUT:", data)

    for key, value in DEFAULT_ROOM.items():
        data.setdefault(key, value)

    # IMPORTANT: normalize BEFORE validation
    data["furniture"] = normalize_furniture(
        data.get("furniture", [])
    )

    print("NORMALIZED OUTPUT:", data)

    room = RoomRequest(**data)

    return room.model_dump()