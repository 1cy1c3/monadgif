import streamlit as st
import functions.gui as gui
import functions.utils as utils
import requests


# Page configuration
st.set_page_config(page_title="MONADSCII", page_icon="assets/media/logo.png")
utils.init_state_gif()
gui.set_bg_hack("assets/media/background.png")
gui.load_header()
gui.load_footer()
gui.load_main_ascii()
with st.sidebar:
    gui.load_sidebar_ascii()
    gui.load_button("ref_buttons")

st.write("\n\n\n")

# Choice: Upload or use a link
option = st.radio("Choose an input method:", ["Upload a GIF", "Enter a GIF URL"])

if option == "Upload a GIF":
    with st.form("upload"):
        uploaded_file = st.file_uploader("Choose an image...", type=['gif'])
        left_col, right_col = st.columns([1, 6])
        with left_col:
            bg_color = st.color_picker("Select Background Color", value="#836EF9")
            font_color = st.color_picker("Select Font Color", value="#60004E")
        with right_col:
            font_size = st.slider("Select Font Size", min_value=1, max_value=10, step=1)
            speed = st.slider("Select Animation Speed", min_value=0.00, max_value=1.00, step=0.05)
        button = st.form_submit_button("Submit")

    if uploaded_file is not None and button:
        file_bytes = uploaded_file.getvalue()
        gui.load_gif(file_bytes, bg_color, font_color, font_size, speed)

elif option == "Enter a GIF URL":
    file_bytes = None
    with st.form("upload"):
        gif_url = st.text_input("Enter the GIF URL:")
        left_col, right_col = st.columns([1, 6])
        with left_col:
            bg_color = st.color_picker("Select Background Color", value="#836EF9")
            font_color = st.color_picker("Select Font Color", value="#60004E")
        with right_col:
            font_size = st.slider("Select Font Size", min_value=1, max_value=10, step=1, value=5)
            speed = st.slider("Select Animation Speed", min_value=0.05, max_value=1.00, step=0.05)
        button = st.form_submit_button("Submit")

    if button and gif_url:
        try:
            response = requests.get(gif_url, stream=True)
            response.raise_for_status()  # This will raise an error for bad responses.
            if "image" not in response.headers["content-type"]:
                st.warning("The provided URL does not point to a valid image.")

            file_bytes = response.content
        except requests.RequestException as e:
            st.warning(f"Failed to fetch the GIF from the URL. Error: {e}")

        if file_bytes is not None:
            gui.load_gif(file_bytes, bg_color, font_color, font_size, speed)