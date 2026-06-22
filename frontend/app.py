import os
import sys

import plotly.graph_objects as go
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="AI Room Designer",
    page_icon="🏠",
    layout="wide"
)

# Allow imports when running: streamlit run frontend/app.py
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from utils.extractor import extract_room_details
from utils.layout_engine import place_furniture


# -----------------------------
# Authentication
# -----------------------------
username = os.getenv("APP_USERNAME")
display_name = os.getenv("APP_NAME")
password_hash = os.getenv("APP_PASSWORD_HASH")

if not all([username, display_name, password_hash]):
    st.error(
        "Missing authentication environment variables. "
        "Please configure APP_USERNAME, APP_NAME, and APP_PASSWORD_HASH in Render."
    )
    st.stop()

credentials = {
    "usernames": {
        username: {
            "name": display_name,
            "password": password_hash,
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "ai_room_designer_v3",
    "abcdef123456",
    cookie_expiry_days=7,
)

name, authentication_status, username = authenticator.login(
    "Login",
    "main"
)

auth_status = st.session_state.get("authentication_status")

if authentication_status is False:
    st.error("Incorrect username or password.")
    st.stop()

if authentication_status is None:
    st.warning("Please log in.")
    st.stop()

authenticator.logout("Logout", "sidebar")

st.sidebar.success(f"Welcome, {name}!")

from utils.extractor import extract_room_details
from utils.layout_engine import place_furniture

import plotly.graph_objects as go


FLOOR_COLORS = {
    "wood": "#8B5A2B",
    "oak": "#A47551",
    "marble": "#E8E8E8",
    "tile": "#B0BEC5",
    "carpet": "#7B5E57",
    "vinyl": "#9E9E9E",
    "laminate": "#A1887F"
}

FURNITURE_COLORS = {
    "queen bed": "#D8D0C8",
    "king bed": "#D8D0C8",
    "single bed": "#D8D0C8",
    "bedside table": "#7A5230",
    "study desk": "#8B5A2B",
    "desk": "#8B5A2B",
    "wardrobe": "#6B4423",
    "sofa": "#607D8B",
    "sectional sofa": "#546E7A",
    "coffee table": "#A1887F",
    "tv unit": "#424242",
    "bookshelf": "#795548",
    "office chair": "#455A64",
    "dining table": "#8D6E63",
    "chair": "#616161",
    "plant": "#4CAF50"
}


def add_box_mesh(fig, x, y, z, l, w, h, color, name):

    vertices_x = [x, x+l, x+l, x, x, x+l, x+l, x]
    vertices_y = [y, y, y+w, y+w, y, y, y+w, y+w]
    vertices_z = [z, z, z, z, z+h, z+h, z+h, z+h]

    i = [0, 0, 0, 1, 4, 4, 3, 3, 0, 0, 1, 1]
    j = [1, 2, 1, 2, 5, 6, 2, 7, 4, 5, 5, 6]
    k = [2, 3, 5, 6, 6, 7, 7, 4, 5, 1, 6, 2]

    fig.add_trace(
        go.Mesh3d(
            x=vertices_x,
            y=vertices_y,
            z=vertices_z,
            i=i,
            j=j,
            k=k,
            color=color,
            opacity=1.0,
            flatshading=False,
            lighting=dict(
                ambient=0.5,
                diffuse=0.9,
                roughness=0.8,
                specular=0.2,
                fresnel=0.1
            ),
            lightposition=dict(
                x=100,
                y=100,
                z=200
            ),
            hovertext=name,
            hoverinfo="text",
            name=name,
            showscale=False
        )
    )

st.title("🏠 AI Room Designer")

st.caption(
    "Describe your room in natural language and generate a 3D layout automatically."
)

prompt = st.text_area(
    "Describe your dream room",
    placeholder=(
        "Example:\n"
        "Create a modern bedroom that is 12 feet by 15 feet with a 9-foot ceiling. "
        "Paint the walls light blue and use wooden flooring. "
        "Add one queen bed, two bedside tables, a study desk, and a wardrobe."
    ),
    height=180
)

if st.button("Generate Room", type="primary"):

    if not prompt.strip():
        st.warning("Please describe your room.")
        st.stop()

    with st.spinner("Designing your room..."):
        room = extract_room_details(prompt)

    left, right = st.columns([1, 2])

    with left:
        st.subheader("Room Details")

        room["room_type"] = st.text_input(
            "Room Type",
            value=room.get("room_type", "living room")
        )

        room["length"] = st.number_input(
            "Length (ft)",
            min_value=1.0,
            value=float(room.get("length", 12)),
            step=1.0
        )

        room["width"] = st.number_input(
            "Width (ft)",
            min_value=1.0,
            value=float(room.get("width", 12)),
            step=1.0
        )

        room["height"] = st.number_input(
            "Height (ft)",
            min_value=1.0,
            value=float(room.get("height", 9)),
            step=1.0
        )

        room["paint_color"] = st.text_input(
            "Paint Color",
            value=room.get("paint_color", "lightblue")
        )

        room["flooring"] = st.text_input(
            "Flooring",
            value=room.get("flooring", "wood")
        )

        st.subheader("Furniture")

        for item in room.get("furniture", []):
            st.write(f"• {item['count']} × {item['type']}")

        with st.expander("View JSON"):
            st.json(room)

    with right:
        st.subheader("3D Preview")

        length = float(room["length"])
        width = float(room["width"])
        height = float(room["height"])

        room_color = room.get("paint_color", "lightblue")

        floor_type = room.get("flooring", "wood").lower()

        floor_color = FLOOR_COLORS.get(
            floor_type,
            "#8B5A2B"
        )

        fig = go.Figure()

        # Floor
        fig.add_trace(
            go.Surface(
                x=[[0, length], [0, length]],
                y=[[0, 0], [width, width]],
                z=[[0, 0], [0, 0]],
                surfacecolor=[[1, 1], [1, 1]],
                colorscale=[
                    [0, floor_color],
                    [1, floor_color]
                ],
                showscale=False,
                opacity=1.0
            )
        )

        # Back wall
        fig.add_trace(
            go.Surface(
                x=[[0, length], [0, length]],
                y=[[0, 0], [0, 0]],
                z=[[0, 0], [height, height]],
                surfacecolor=[[1, 1], [1, 1]],
                colorscale=[
                    [0, room_color],
                    [1, room_color]
                ],
                showscale=False,
                opacity=0.95
            )
        )

        # Left wall
        fig.add_trace(
            go.Surface(
                x=[[0, 0], [0, 0]],
                y=[[0, width], [0, width]],
                z=[[0, 0], [height, height]],
                surfacecolor=[[1, 1], [1, 1]],
                colorscale=[
                    [0, room_color],
                    [1, room_color]
                ],
                showscale=False,
                opacity=0.95
            )
        )

        # Window
        fig.add_trace(
            go.Surface(
                x=[[length * 0.25, length * 0.45],
                [length * 0.25, length * 0.45]],
                y=[[0.02, 0.02],
                [0.02, 0.02]],
                z=[[height * 0.35, height * 0.35],
                [height * 0.7, height * 0.7]],
                surfacecolor=[[1, 1], [1, 1]],
                colorscale=[
                    [0, "#B3E5FC"],
                    [1, "#B3E5FC"]
                ],
                showscale=False,
                opacity=0.35
            )
        )

        # Door
        add_box_mesh(
            fig,
            x=length * 0.75,
            y=width - 0.2,
            z=0,
            l=3,
            w=0.2,
            h=7,
            color="#5D4037",
            name="Door"
        )

        placements = place_furniture(room)

        for furniture in placements:

            furniture_type = furniture["type"].lower()

            color = FURNITURE_COLORS.get(
                furniture_type,
                "#A1887F"
            )

            add_box_mesh(
                fig,
                x=furniture["x"],
                y=furniture["y"],
                z=furniture["z"],
                l=furniture["length"],
                w=furniture["width"],
                h=furniture["height"],
                color=color,
                name=furniture["type"]
            )

        fig.update_layout(
            scene=dict(
                aspectmode="data",

                xaxis=dict(
                    title="Length (ft)",
                    showbackground=False,
                    showgrid=False,
                    zeroline=False
                ),

                yaxis=dict(
                    title="Width (ft)",
                    showbackground=False,
                    showgrid=False,
                    zeroline=False
                ),

                zaxis=dict(
                    title="Height (ft)",
                    showbackground=False,
                    showgrid=False,
                    zeroline=False
                ),

                camera=dict(
                    eye=dict(
                        x=1.9,
                        y=2.2,
                        z=1.5
                    ),
                    up=dict(
                        x=0,
                        y=0,
                        z=1
                    )
                )
            ),

            height=700,

            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0
            ),

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )
    