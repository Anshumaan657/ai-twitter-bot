from google import genai

from config import GEMINI_API_KEY
from services.logger import logger


# Configure Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_gemini_response(prompt: str) -> str:
    """
    Generate response using Gemini API.
    """

    try:

        logger.info("Sending request to Gemini")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        logger.info("Gemini response generated successfully")

        return response.text

    except Exception as error:

        logger.error(f"Gemini API Error: {error}")

        return "Error generating response."