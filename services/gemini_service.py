import google.generativeai as genai

from config import GEMINI_API_KEY
from services.logger import logger

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_text(prompt: str) -> str:
    """
    Generate text using Gemini.
    """

    try:
        response = model.generate_content(prompt)

        logger.info("Gemini response generated successfully")

        return response.text.strip()

    except Exception as e:
        logger.error(f"Gemini API Error: {e}")

        return "Error generating response."