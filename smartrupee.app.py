# Internal Pinterest Automation Tool (MVP)
# Built for solo creator usage using Streamlit + OpenAI + DALL·E

import streamlit as st
import openai
from PIL import Image
import base64
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="SmartRupee Pin Generator", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store your key in .streamlit/secrets.toml

# --- UI ---
st.title("📌 Pinterest Pin Generator")
st.markdown("Generate Pinterest-ready pin content + images for your niche")

# --- Input Form ---
with st.form("pin_form"):
    topic = st.text_input("Enter a topic or keyword", "Smart saving tips")
    niche = st.selectbox("Select your niche", ["Personal Finance", "Health & Wellness", "DIY", "Travel", "Lifestyle"])
    tone = st.selectbox("Select tone", ["Informative", "Inspiring", "Trendy", "Conversational"])
    submit = st.form_submit_button("Generate Pin Content")

# --- OpenAI Prompt Builder ---
def generate_text(topic, niche, tone):
    prompt = f"Write a Pinterest pin title and description for the topic: '{topic}' in the niche of {niche}. Tone: {tone}. Keep title under 80 characters and description under 200 characters."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# --- DALL·E Image Generation ---
def generate_dalle_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="b64_json"
    )
    image_data = base64.b64decode(response["data"][0]["b64_json"])
    image = Image.open(io.BytesIO(image_data))
    return image

# --- Processing ---
if submit:
    with st.spinner("Generating pin content..."):
        pin_text = generate_text(topic, niche, tone)
        st.subheader("📝 Generated Pin Content")
        st.markdown(pin_text)

    with st.spinner("Creating pin image with DALL·E..."):
        dalle_prompt = f"Pinterest-style graphic with the theme: {topic}, visually appealing for {niche.lower()} audience"
        image = generate_dalle_image(dalle_prompt)
        st.subheader("📷 AI-Generated Pin Image")
        st.image(image, caption="Generated via DALL·E", use_column_width=True)

        # Offer download
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.download_button("Download Pin Image", data=buf.getvalue(), file_name=f"{topic}.png", mime="image/png")
