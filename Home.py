import streamlit as st
import functions.gui as gui
import functions.utils as utils
import requests


# Page configuration
st.set_page_config(page_title="GIF2ASCII", page_icon="assets/media/logo.png")
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
    uploaded_file = st.file_uploader("Choose an image...", type=['gif'])
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        gui.load_gif(file_bytes)

elif option == "Enter a GIF URL":
    gif_url = st.text_input("Enter the GIF URL:")
    if gif_url:
        try:
            response = requests.get(gif_url, stream=True)
            response.raise_for_status()  # This will raise an error for bad responses.
            if "image" not in response.headers["content-type"]:
                st.warning("The provided URL does not point to a valid image.")

            file_bytes = response.content
            gui.load_gif(file_bytes)
        except requests.RequestException as e:
            st.warning(f"Failed to fetch the GIF from the URL. Error: {e}")
