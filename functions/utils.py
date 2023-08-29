import streamlit as st

ss = st.session_state


def init_state_gif():
    if "width" not in ss:
        ss["width"] = 0
    if "height" not in ss:
        ss["height"] = 0
