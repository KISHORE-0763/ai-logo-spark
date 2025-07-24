# ==============================================================================
# AI Logo Spark: Your Personal Design Assistant
# Version: 1.0 (Stable - Powered by OpenAI's DALL-E 3)
#
# This application generates professional logo concepts from a user's description.
# It uses the stable and reliable DALL-E 3 model via the OpenAI API.
# ==============================================================================

import streamlit as st
import openai

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

# This function takes the user's simple description and engineers a detailed,
# high-quality prompt for the DALL-E 3 image generation model.

def create_logo_prompt(company_description, logo_style, color_palette):
    """Engineers a detailed prompt for the DALL-E 3 model."""
    
    # Base prompt structure
    base_prompt = (
        f"A modern, clean, vector logo for a company. "
        f"The company is: '{company_description}'. "
        f"The logo style should be: '{logo_style}'. "
        f"Use the color palette: '{color_palette}'. "
        "The logo should be on a clean, white background, suitable for branding. "
        "Avoid realistic 3D rendering. The logo must be simple, memorable, and professional. "
        "Do not include any text unless it's an abstract part of the logo."
    )
    return base_prompt

def generate_logo_concepts(prompt):
    """Calls the OpenAI DALL-E 3 API to generate logo images."""
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=4,  # Generate 4 different concepts
            size="1024x1024",
            quality="standard",
        )
        # Extract the image URLs from the response
        image_urls = [data.url for data in response.data]
        return image_urls
    except Exception as e:
        # Handle potential errors, like content policy violations or API issues
        st.error(f"An error occurred while generating images: {e}", icon="🔥")
        return None

# ==============================================================================
# 3. STREAMLIT UI (The Frontend)
# ==============================================================================

st.title("AI Logo Spark 🎨✨")
st.write("Turn your ideas into professional logo concepts in seconds. Describe your business and let AI do the rest.")
st.divider()

# --- User Input Form ---
with st.form(key="logo_form"):
    st.subheader("Describe Your Vision")

    # 1. Company Description
    desc_input = st.text_area(
        "**What does your company or project do?**",
        height=100,
        placeholder="e.g., A coffee shop that uses sustainably sourced beans and has a cozy, rustic atmosphere."
    )

    # 2. Logo Style
    style_input = st.selectbox(
        "**Choose a logo style:**",
        ("Minimalist", "Geometric", "Abstract", "Vintage", "Playful", "Corporate")
    )

    # 3. Color Palette
    color_input = st.text_input(
        "**Describe a color palette:**",
        placeholder="e.g., Earthy tones like brown, green, and beige"
    )

    # Submit button for the form
    submit_button = st.form_submit_button(label="Spark My Logos!", use_container_width=True)

# --- Logo Generation and Display ---
if submit_button:
    if not desc_input or not color_input:
        st.warning("Please fill out all the fields to generate your logos.", icon="⚠️")
    else:
        with st.spinner("Our AI designer is sketching your concepts... This might take a moment."):
            # Engineer the detailed prompt
            final_prompt = create_logo_prompt(desc_input, style_input, color_input)
            
            # Generate the images
            logo_urls = generate_logo_concepts(final_prompt)

        if logo_urls:
            st.divider()
            st.subheader("Here Are Your AI-Generated Logo Concepts!")
            
            # Display the 4 logos in a 2x2 grid
            cols = st.columns(4)
            for i, url in enumerate(logo_urls):
                with cols[i % 4]:
                    st.image(url, caption=f"Concept #{i+1}", use_column_width=True)
                    # Add a download button for each image
                    st.download_button("Download", requests.get(url).content, file_name=f"logo_concept_{i+1}.png", mime="image/png")
        else:
            st.error("Could not generate logo concepts. The AI may have flagged the prompt, or an API error occurred.", icon="🚨")
