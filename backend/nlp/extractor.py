from shared.schemas import RoomRequest, Furniture


def extract_room_details(user_prompt: str) -> RoomRequest:

    return RoomRequest(
        room_type="living room",
        length=18,
        width=14,
        height=10,
        paint_color="light blue",
        flooring="wood",
        furniture=[
            Furniture(type="sofa", count=1),
            Furniture(type="coffee table", count=1),
            Furniture(type="floor lamp", count=2),
        ],
    )