import io
import base64

import functions.ascii as gif
import streamlit as st

ss = st.session_state


def set_bg_hack(main_bg):
    # set bg name
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


def load_button(name):
    if name == "ref_buttons":
        with open("style/ref_buttons.css", "r") as f:
            ref_buttons_css = f.read()
        st.markdown(ref_buttons_css, unsafe_allow_html=True)


def load_gif(file_bytes):
    frames = gif.extract_frames_as_bytesio(io.BytesIO(file_bytes))
    ascii_gif = gif.generate_ascii_gif(frames)
    st.image(ascii_gif, caption="ASCII Animation", use_column_width=True)

    ascii_gif_data = ascii_gif.getvalue()
    st.download_button(label="Download GIF", data=ascii_gif_data, file_name="gifs-by-1cy1c3.gif", mime="image/gif")


def load_main_ascii():
    gif_col, left_col, right_col = st.columns([1, 1, 3])
    with right_col:
        st.markdown("# GIF 2 ASCII")
        st.markdown("This project is dedicated to the MONAD Community!")
        st.markdown("Have fun generating some ascii art")
    with left_col:
        st.image("assets/media/logo.png")

    with gif_col:
        st.image("assets/media/pepe_dance.gif")


def load_sidebar_ascii():
    with open("text/sidebar_ascii.txt") as file:
        sidebar_txt = file.read()
    with st.sidebar:
        st.write(sidebar_txt, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_header():
    with open("style/header.css") as f:
        header_css = f.read()
    st.markdown(header_css, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_footer():
    with open("style/footer.css") as f:
        footer_css = f.read()
    st.markdown(footer_css, unsafe_allow_html=True)
