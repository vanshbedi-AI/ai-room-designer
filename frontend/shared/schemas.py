from pydantic import BaseModel
from typing import List, Optional


class Furniture(BaseModel):
    type: str
    count: int = 1


class RoomRequest(BaseModel):
    room_type: str
    length: float
    width: float
    height: float = 9.0
    paint_color: str
    flooring: str
    furniture: List[Furniture]


class RoomResponse(BaseModel):
    success: bool
    room_data: RoomRequest