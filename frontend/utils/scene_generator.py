import tempfile
import trimesh


def generate_room(room_data):

    length = room_data["length"]
    width = room_data["width"]
    height = room_data["height"]

    room = trimesh.creation.box(
        extents=[length, width, height]
    )

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".stl",
        delete=False
    )

    room.export(temp_file.name)

    return temp_file.name