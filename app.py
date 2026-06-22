import streamlit as st
import requests
from PIL import Image
import io

# வெப்சைட் தலைப்பு
st.set_page_config(page_title="AI Image Generator", layout="centered")
st.title("📸 AI Image Generator Website")
st.write("உங்கள் புகைப்படம் மற்றும் விவரங்களை வழங்கி புதிய படத்தை உருவாக்குங்கள்.")

# 1. பயனரிடம் இருந்து விவரங்களை பெறுதல்
uploaded_file = st.file_uploader("1. உங்கள் புகைப்படத்தை பதிவேற்றவும் (Upload Photo):", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # பதிவேற்றிய படத்தை திரையில் காட்டுதல்
    image = Image.open(uploaded_file)
    st.image(image, caption="நீங்கள் பதிவேற்றிய படம்", use_column_width=True)

# 2. டெக்ஸ்ட் விவரங்கள் (Prompt)
text_prompt = st.text_area("2. உங்களுக்கு படம் எப்படி மாற வேண்டும் என்ற விவரங்களை எழுதவும் (Prompt):", 
                           placeholder="உதாரணமாக: Change background to a beautiful beach, cinematic lighting, realistic...")

# 3. படம் உருவாக்கும் பட்டன்
if st.button("Generate New Image ✨"):
    if uploaded_file is not None and text_prompt != "":
        st.info("உங்கள் படம் உருவாக்கப்படுகிறது... தயவுசெய்து காத்திருக்கவும்.")
        
        try:
            # குறிப்பு: இங்கு உங்கள் AI API (உதா: Stability AI / Hugging Face) முகவரியை இணைக்க வேண்டும்
            # இது ஒரு மாதிரி (Example) API அழைப்பு மட்டுமே
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            headers = {"Authorization": "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"} # உங்கள் API Key-ஐ இங்கு இட வேண்டும்
            
            # கோப்பை AI-க்கு அனுப்ப தயார் செய்தல்
            bytes_data = uploaded_file.getvalue()
            
            # AI-க்கு அனுப்பும் தரவு (உங்களுடைய Text Prompt மற்றும் Image)
            payload = {
                "inputs": text_prompt,
                "image": bytes_data
            }
            
            # API-க்கு கோரிக்கை அனுப்புதல்
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                # புதிய படத்தை பெற்று காட்டுதல்
                output_image = Image.open(io.BytesIO(response.content))
                st.success("வெற்றிகரமாக உருவாக்கப்பட்டது!")
                st.image(output_image, caption="உருவாக்கப்பட்ட புதிய படம்", use_column_width=True)
            else:
                st.error("API இணைப்பில் ஏதோ தவறு நடந்துள்ளது. (API Key-ஐ சரிபார்க்கவும்)")
                
        except Exception as e:
            st.error(f"தவறு நடந்துள்ளது: {e}")
            
    else:
        st.warning("தயவுசெய்து புகைப்படத்தையும், விவரங்களையும் முழுமையாக வழங்கவும்!")
