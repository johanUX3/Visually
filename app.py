

import streamlit as st
from PIL import Image, ImageEnhance
import io
from backend import analyze_image_prompt, generate_styling_suggestions
import time

from streamlit_lottie import st_lottie
import requests
st.set_page_config(
    page_title="Visually 🎨",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto",
)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #1E90FF, #FF6347); 
    }
    </style>
""", unsafe_allow_html=True)





st.title("🧠 Visually")
st.subheader("Upload an image and get smart feedback on your prompt!")










# Function to adjust brightness (can be expanded for other edits)
def adjust_brightness(image):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(1.5)  # Brightness adjustment factor

# Function to save image for download
def save_image_for_download(image):
    img_io = io.BytesIO()
    image.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

# Streamlit File Uploader and Text Area for Prompt
uploaded_file = st.file_uploader("📂 Upload an image", type=["png", "jpg", "jpeg"])
user_prompt = st.text_area("💬 Describe what you expect or feel from the image:")
caption, feedback = analyze_image_prompt(uploaded_file, user_prompt)
styling_suggestions = generate_styling_suggestions(uploaded_file, user_prompt)
if uploaded_file:
    try:
        image = Image.open(uploaded_file)  # Try to open the image
        # If successful, process the image
        caption, feedback = analyze_image_prompt(uploaded_file, user_prompt)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    except Exception as e:
        st.error("Error opening image: " + str(e))

if uploaded_file and user_prompt:
    if st.button("🔍 Analyze Image vs Prompt"):
        with st.spinner("Analyzing... please wait..."):
            # 🔄 Show Lottie animation during analysis
            
            # Perform analysis
            caption, feedback = analyze_image_prompt(uploaded_file, user_prompt)

        # ✅ Spinner and animation end here
        st.success("✅ Analysis complete!")

        # 🔠 AI Caption Output
        st.subheader("🖼️ AI-Generated Caption:")
        st.write(caption)

        # 📊 Feedback
        st.subheader("📊 Feedback & Suggestions:")
        st.markdown(feedback)

        # 🎨 Styling Suggestions
        styling_suggestions = generate_styling_suggestions(uploaded_file, user_prompt)
        st.subheader("🎨 Styling Suggestions:")
        for suggestion in styling_suggestions:
            st.write(f"- {suggestion}")

        # 🖼️ Process Image + Download
        try:
            uploaded_image = Image.open(uploaded_file)
            processed_image = adjust_brightness(uploaded_image)

            # Save to download
            img_io = save_image_for_download(processed_image)

            st.subheader("⬇️ Download Processed Image")
            st.download_button(
                label="Download Processed Image",
                data=img_io,
                file_name="processed_image.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"❌ Error processing the image: {str(e)}")




