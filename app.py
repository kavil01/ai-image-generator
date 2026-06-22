import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="AI Image Generator", layout="centered")
st.title("🎨 AI Image Generator Website")
st.write("நீங்கள் விரும்பும் படத்தின் விவரங்களை கீழே டைப் செய்து புதிய படத்தை உருவாக்குங்கள்.")

user_prompt = st.text_input("உங்களுக்கு தேவையான படத்தின் விவரங்களை எழுதவும் (Prompt):", 
                            placeholder="உதாரணமாக: A beautiful nature landscape, 4k...")

if st.button("Generate Image ✨"):
    if user_prompt.strip() != "":
        st.info("உங்கள் கற்பனைக்கேற்ப படம் உருவாக்கப்படுகிறது... தயவுசெய்து காத்திருக்கவும்.")
        
        try:
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            
            # 🛑 உங்கள் Hugging Face API Key-ஐ (hf_...) கீழே உள்ள " " க்குள் சரியாகப் போடவும்
            headers = {"Authorization": "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"}
            
            payload = {"inputs": user_prompt}
            
            # தரவைச் சரியாக அனுப்புதல்
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                st.success("வெற்றிகரமாக உருவாக்கப்பட்டது!")
                st.image(image, caption=f"உருவாக்கப்பட்ட படம்: {user_prompt}", use_container_width=True)
            else:
                st.error(f"API Error! Status Code: {response.status_code}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"ஏதோ ஒரு தவறு நடந்துள்ளது: {e}")
    else:
        st.warning("தயவுசெய்து ஏதேனும் ஒரு விவரத்தை (Prompt) டைப் செய்யவும்!")
