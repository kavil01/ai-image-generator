import streamlit as st
import requests
import io
from PIL import Image

# வெப்சைட் வடிவமைப்பு
st.set_page_config(page_title="AI Image Generator", layout="centered")
st.title("🎨 AI Image Generator Website")
st.write("நீங்கள் விரும்பும் படத்தின் விவரங்களை கீழே டைப் செய்து புதிய படத்தை உருவாக்குங்கள்.")

# 1. விவரங்களை வாங்குவதற்கான Text Input பெட்டி
user_prompt = st.text_input("உங்களுக்கு தேவையான படத்தின் விவரங்களை எழுதவும் (Prompt):", 
                            placeholder="உதாரணமாக: A futuristic city, 4k, cinematic...")

# 2. படம் உருவாக்கும் பட்டன்
if st.button("Generate Image ✨"):
    if user_prompt.strip() != "":
        st.info("உங்கள் கற்பனைக்கேற்ப படம் உருவாக்கப்படுகிறது... தயவுசெய்து காத்திருக்கவும்.")
        
        try:
            # நிலையான, இலவசமாகப் பயன்படுத்தக்கூடிய Stable Diffusion XL மாடல்
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            
            # 🛑 முக்கியம்: 'YOUR_HF_API_KEY' என்ற இடத்தில் உங்களுடைய Hugging Face டோக்கனை (hf_...) அப்படியே பேஸ்ட் செய்யவும்
            headers = {"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"}
            
            payload = {"inputs": user_prompt}
            
            # API-க்கு சரியான முறையில் JSON வடிவில் தரவை அனுப்புதல்
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                # படமாக மாற்றி திரையில் காட்டுதல்
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                
                st.success("வெற்றிகரமாக உருவாக்கப்பட்டது!")
                st.image(image, caption=f"உருவாக்கப்பட்ட படம்: {user_prompt}", use_container_width=True)
                
            else:
                st.error(f"API Error! Status Code: {response.status_code}")
                st.write("விளக்கம்:", response.text)
                
        except Exception as e:
            st.error(f"ஏதோ ஒரு தவறு நடந்துள்ளது: {e}")
            
    else:
        st.warning("தயவுசெய்து ஏதேனும் ஒரு விவரத்தை (Prompt) டைப் செய்யவும்!")