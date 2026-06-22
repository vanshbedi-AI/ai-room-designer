from utils.furniture_catalog import FURNITURE

def place_furniture(room):

    placements = {}

    for item in room["furniture"]:

        if "bed" in item["type"].lower():
            placements[item["type"]] = (1, 1)

        elif "wardrobe" in item["type"].lower():
            placements[item["type"]] = (
                room["length"] - 4,
                1
            )

    return placements

def overlaps(a, b):

    return not (
        a["x"] + a["length"] <= b["x"]
        or b["x"] + b["length"] <= a["x"]
        or a["y"] + a["width"] <= b["y"]
        or b["y"] + b["width"] <= a["y"]
    )

def find_position(
    room_length,
    room_width,
    length,
    width,
    placed
):

    step = 1

    y = 0

    while y <= room_width - width:

        x = 0

        while x <= room_length - length:

            candidate = {
                "x": x,
                "y": y,
                "length": length,
                "width": width
            }

            if not any(
                overlaps(candidate, item)
                for item in placed
            ):
                return x, y

            x += step

        y += step

    return None


def place_furniture(room):

    placed = []

    for item in room["furniture"]:

        name = item["type"].lower()

        config = FURNITURE.get(
            name,
            {"size": (2, 2, 2)}
        )

        length, width, height = config["size"]

        position = find_position(
            room["length"],
            room["width"],
            length,
            width,
            placed
        )

        if position:

            x, y = position

            placed.append({
                "type": name,
                "x": x,
                "y": y,
                "z": 0,
                "length": length,
                "width": width,
                "height": height
            })

    return placed