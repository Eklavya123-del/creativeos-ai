
import os

from google import genai
from google.genai import types


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_gemini_creative(

    campaign_brief: str,

    headline: str,

    template_style: str,

    ratio: str,

    product_name: str
):

    prompt = f"""
    Create a premium wellness supplement advertisement.

    Campaign:
    {campaign_brief}

    Headline:
    {headline}

    Product:
    {product_name}

    Style:
    {template_style}

    Ratio:
    {ratio}

    The advertisement should feel:
    - cinematic
    - premium
    - luxury wellness
    - modern
    - clean composition
    - realistic product photography
    - elegant lighting
    - highly aesthetic

    Ensure:
    - strong typography hierarchy
    - realistic product placement
    - premium shadows
    - depth
    - award-winning ad composition
    """

    response = client.models.generate_content(

        model="gemini-2.0-flash-preview-image-generation",

        contents=prompt,

        config=types.GenerateContentConfig(
            response_modalities=[
                "TEXT",
                "IMAGE"
            ]
        )
    )

    for part in response.candidates[0].content.parts:

        if part.inline_data:

            image_bytes = part.inline_data.data

            
            output_dir = os.path.join(
                os.path.dirname(__file__),
                "outputs"
            )



            os.makedirs(
                output_dir,
                exist_ok=True
            )

            output_path = os.path.join(
                output_dir,
                "generated_ai_creative.png"
            )

            with open(
                output_path,
                "wb"
            ) as f:

                f.write(image_bytes)

            return "/outputs/generated_ai_creative.png"

    return None

