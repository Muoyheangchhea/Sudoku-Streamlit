import streamlit as st

st.set_page_config(
    page_title="Sudoku Game",
    page_icon="🎮",
)

st.write("# Welcome to Sudoku Game! 🎮")

st.sidebar.success("Select an option above.")

st.markdown(
    """ This is Sudoku Game. We have two modes that you can play based on your preference. 
    1. Play Sudoku (Classic Mode): playing using your own skill.
    2. Play Sudoku (Practice Mode): practicing and learning how to play Sudoku.

    **Note**: Select the sidebar to choose the mode you want and read the instruction carefully before you play.

    *We hope you enjoy your game* - :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:
"""
)

