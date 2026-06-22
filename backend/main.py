from fastapi import FastAPI
from shared.schemas import RoomResponse
from backend.nlp.extractor import extract_room_details

app = FastAPI(title="AI Room Designer")


@app.post("/generate", response_model=RoomResponse)
def generate_room(payload: dict):

    room = extract_room_details(payload["prompt"])

    return {
        "success": True,
        "room_data": room
    }