import streamlit as st
from streamlit_stl import stl_from_file

from utils.extractor import extract_room_details
from utils.scene_generator import generate_room


st.set_page_config(
    page_title="AI Room Designer",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 AI Room Designer")

prompt = st.text_area(
    "Describe your dream room",
    height=150
)

if st.button("Generate Design"):

    with st.spinner("Understanding your room..."):

        room = extract_room_details(prompt)
        st.write(room)

    left, right = st.columns([1, 2])

    with left:

        st.subheader("Extracted Details")

        room["length"] = st.number_input(
            "Length",
            value=float(room.get("length", 12))
        )

        room["width"] = st.number_input(
            "Width",
            value=float(room.get("width", 12))
        )

        room["height"] = st.number_input(
            "Height",
            value=float(room.get("height", 9))
        )

        room["paint_color"] = st.text_input(
            "Paint",
            value=room["paint_color"]
        )

        st.json(room)

    with right:

        st.subheader("3D Preview")

        file_path = generate_room(room)

        stl_from_file(
            file_path=file_path,
            color="#87CEEB"
        )

with open("frontend/styles/main.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )