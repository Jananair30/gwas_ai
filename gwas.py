import os
from openai import OpenAI
from PIL import Image
import streamlit as st
import requests
from gwasMethods import gwasMethods as gwas

client = OpenAI(api_key=st.secrets["OPEN_API_KEY"])

def display_image(image_url):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        img = Image.open(response.raw)
        st.image(img, caption='Cover Image')

def create_sidebar_navigation():
    if "navigation" not in st.session_state:
        st.session_state.navigation = False  # Initialize the navigation attribute

    if st.button("Toggle Navigation"):
        st.session_state.navigation = not st.session_state.navigation  # Toggle the navigation attribute

    if st.session_state.navigation:
        st.sidebar.header("Navigation")
        st.sidebar.subheader("Sections")
        st.sidebar.write("Link 1")
        st.sidebar.write("Link 2")
        st.sidebar.write("Link 3")

def main():
    create_sidebar_navigation()  # Call the function to create the sidebar navigation

    st.title("Gym Workout Activity Suggestor (GWAS.ai)")

    age_range = st.slider("Select Your Age Range:", 10, 100, (20, 50))

    with st.expander("User Options", expanded=False):
        user_option = st.radio("Select User Type:", ("Students", "Athletes", "Sport Teacher", "Random User"))

    workout_input = st.text_input("Enter your workout goal or body part focus:", "")
    if workout_input:
        workout_suggestion = gwas.gym_ai(workout_input, client)
        design_prompt = gwas.design_ai(workout_input, client)
        image_url = gwas.cover_ai(design_prompt, client)

        st.write("Workout Suggestion:")
        st.write(workout_suggestion)
        st.divider()

    if st.button("Generate Cover Image"):
        st.write("Cover Image:")
        display_image(image_url)

if __name__ == "__main__":
    main()