# Final Streamlit app code (compatible with OpenAI v1.x)

import streamlit as st
import openai
from PIL import Image
import base64
import io

# Set up Streamlit page
st.set_page_config(page_title="SmartRupee Pin Generator", layout="centered")

# Initialize OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# UI Header
st.title("📌 Pinterest Pin Generator")
st.markdown("Generate Pinterest-ready pin content + images for your niche")

# Input form
with st.form("pin_form"):
    topic = st.text_input("Enter a topic or keyword", "Smart saving tips")
    niche = st.selectbox("Select your niche", ["Personal Finance", "Health & Wellness", "DIY", "Travel", "Lifestyle"])
    tone = st.selectbox("Select tone", ["Informative", "Inspiring", "Trendy", "Conversational"])
    submit = st.form_submit_button("Generate Pin Content")

# Function to generate text
def generate_text(topic, niche, tone):
    prompt = f"Create a Pinterest pin title and description for a post about '{topic}' in the niche of '{niche}' with a '{tone}' tone. Format it as:\nTitle: ...\nDescription: ..."
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    text = response.choices[0].message.content.strip()
    return text

# Placeholder image function (replace with DALL·E if needed)
def generate_image(topic):
    from PIL import ImageDraw
    img = Image.new('RGB', (800, 1200), color=(230, 255, 240))
    d = ImageDraw.Draw(img)
    d.text((50, 600), topic, fill=(0, 100, 0))
    return img

# Process submission
if submit:
    with st.spinner("Generating pin content..."):
        pin_text = generate_text(topic, niche, tone)
        st.subheader("📝 Generated Pin Content")
        st.markdown(pin_text)
        
        st.subheader("📷 Sample Pin Image")
        image = generate_image(topic)
        st.image(image, caption="Placeholder Image", use_column_width=True)
        
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.download_button("Download Pin Image", data=buf.getvalue(), file_name=f"{topic}.png", mime="image/png")
