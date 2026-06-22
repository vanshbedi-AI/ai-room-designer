import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="AI Room Designer",
    page_icon="🏠",
    layout="wide"
)

import os
import sys
import plotly.graph_objects as go
from utils.extractor import extract_room_details
from utils.layout_engine import place_furniture

authenticator.login()

if st.session_state.get("authentication_status") is False:
    st.error("Incorrect username or password.")
    st.stop()

if st.session_state.get("authentication_status") is None:
    st.warning("Please log in.")
    st.stop()

authenticator.logout("Logout", "sidebar")

st.sidebar.success(
    f"Welcome, {st.session_state['name']}!"
)

    



        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )

    def add_box_wireframe(
        fig,
        x,
        y,
        z,
        length,
        width,
        height,
        color="brown",
        name=""
    ):
        """Draw a 3D cuboid as a wireframe."""

        vertices = [
            (x, y, z),
            (x + length, y, z),
            (x + length, y + width, z),
            (x, y + width, z),
            (x, y, z + height),
            (x + length, y, z + height),
            (x + length, y + width, z + height),
            (x, y + width, z + height),
        ]

        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # floor
            (4, 5), (5, 6), (6, 7), (7, 4),  # ceiling
            (0, 4), (1, 5), (2, 6), (3, 7)   # vertical
        ]

        for start, end in edges:
            fig.add_trace(
                go.Scatter3d(
                    x=[vertices[start][0], vertices[end][0]],
                    y=[vertices[start][1], vertices[end][1]],
                    z=[vertices[start][2], vertices[end][2]],
                    mode="lines",
                    line=dict(
                        color=color,
                        width=6
                    ),
                    hoverinfo="text",
                    text=name,
                    showlegend=False
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
                st.write(
                    f"• {item['count']} × {item['type']}"
                )

            with st.expander("View JSON"):
                st.json(room)

        with right:
            st.subheader("3D Preview")

            length = float(room.get("length", 12))
            width = float(room.get("width", 12))
            height = float(room.get("height", 9))

            room_color = room.get(
                "paint_color",
                "lightblue"
            )

            fig = go.Figure()

            # Draw room wireframe
            add_box_wireframe(
                fig,
                x=0,
                y=0,
                z=0,
                length=length,
                width=width,
                height=height,
                color=room_color,
                name="Room"
            )

            # Draw furniture
            placements = place_furniture(room)

            for furniture in placements:

                add_box_wireframe(
                    fig,
                    x=furniture["x"],
                    y=furniture["y"],
                    z=furniture["z"],
                    length=furniture["length"],
                    width=furniture["width"],
                    height=furniture["height"],
                    color="#8B4513",
                    name=furniture["type"]
                )

            fig.update_layout(
                scene=dict(
                    aspectmode="data",
                    xaxis=dict(
                        title="Length (ft)"
                    ),
                    yaxis=dict(
                        title="Width (ft)"
                    ),
                    zaxis=dict(
                        title="Height (ft)"
                    ),
                    camera=dict(
                        eye=dict(
                            x=1.6,
                            y=1.6,
                            z=1.3
                        )
                    )
                ),
                height=700,
                margin=dict(
                    l=0,
                    r=0,
                    t=0,
                    b=0
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

