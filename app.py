# ==============================================================================
# AI Logo Spark: Your Personal Design Assistant
# Version: 1.1 (Stable - DALL-E 3 API Fix)
#
# This version corrects the API call to DALL-E 3. The model now only accepts
# n=1 (one image per request). This code has been updated to make four
# separate requests to generate the four logo concepts.
# ==============================================================================

import streamlit as st
import openai
import requests # Need this for the download button

# ==============================================================================
# 1. PAGE CONFIGURATION & API KEY MANAGEMENT
# ==============================================================================

st.set_page_config(
    page_title="AI Logo Spark",
    page_icon="🎨",
    layout="wide"
)

# Securely load the OpenAI API key from Streamlit's secrets management
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API Key not found. Please add it to your Streamlit secrets.", icon="🚨")
    st.stop()

# ==============================================================================
# 2. AI PROMPT ENGINEERING FOR LOGO DESIGN
# ==============================================================================

def create_logo_prompt(company_description, logo_style, color_palette):
    """Engineers a detailed prompt for the DALL-E 3 model."""
    base_prompt = (
        f"A modern, clean, vector logo for a company. "
        f"The company is: '{company_description}'. "
        f"The logo style should be: '{logo_style}'. "
        f"Use the color palette: '{color_palette}'. "
        "The logo should be on a clean, solid white background, suitable for branding. "
        "The design must be simple, memorable, and professional. "
        "Avoid 3D rendering and complex text. The logo should be iconic."
    )
    return base_prompt

# --- THIS FUNCTION IS NOW CORRECTED ---
def generate_logo_concepts(prompt, num_images=4):
    """Calls the OpenAI DALL-E 3 API multiple times to generate concepts."""
    image_urls = []
    try:
        # Loop to make multiple requests, since n must be 1
        for i in range(num_images):
            st.toast(f"Generating concept #{i+1}...")
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,  # Generate 1 image at a time
                size="1024x1024",
                quality="standard",
            )
            # Add the URL of the single generated image to our list
            image_urls.append(response.data[0].url)
        return image_urls
    except Exception as e:
        st.error(f"An error occurred while generating images: {e}", icon="🔥")
        return None

# ==============================================================================
# 3. STREAMLIT UI (The Frontend)
# ==============================================================================

st.title("AI Logo Spark 🎨✨")
st.write("Turn your ideas into professional logo concepts in seconds. Describe your business and let AI do the rest.")
st.divider()

with st.form(key="logo_form"):
    st.subheader("Describe Your Vision")

    desc_input = st.text_area(
        "**What does your company or project do?**",
        height=100,
        placeholder="e.g., A coffee shop that uses sustainably sourced beans and has a cozy, rustic atmosphere."
    )
    style_input = st.selectbox(
        "**Choose a logo style:**",
        ("Minimalist", "Geometric", "Abstract", "Vintage", "Playful", "Corporate")
    )
    color_input = st.text_input(
        "**Describe a color palette:**",
        placeholder="e.g., Earthy tones like brown, green, and beige"
    )

    submit_button = st.form_submit_button(label="Spark My Logos!", use_container_width=True)

if submit_button:
    if not desc_input or not color_input:
        st.warning("Please fill out all the fields to generate your logos.", icon="⚠️")
    else:
        with st.spinner("Our AI designer is sketching your concepts... This might take up to a minute."):
            final_prompt = create_logo_prompt(desc_input, style_input, color_input)
            logo_urls = generate_logo_concepts(final_prompt)

        if logo_urls:
            st.divider()
            st.subheader("Here Are Your AI-Generated Logo Concepts!")
            
            cols = st.columns(4)
            for i, url in enumerate(logo_urls):
                with cols[i % 4]:
                    st.image(url, caption=f"Concept #{i+1}", use_column_width=True)
                    try:
                        # Fetch the image content for the download button
                        image_content = requests.get(url).content
                        st.download_button("Download", image_content, file_name=f"logo_concept_{i+1}.png", mime="image/png")
                    except Exception as e:
                        st.error("Could not create download link.", icon="⚠️")
        else:
            st.error("Could not generate logo concepts. The AI may have flagged the prompt, or an API error occurred.", icon="🚨")
