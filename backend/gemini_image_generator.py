import os

from google import genai
from google.genai import types


client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)


def generate_gemini_creative(

    campaign_brief: str,

    headline: str,

    template_style: str,

    ratio: str,

    product_name: str,

    template_data: dict = None
):

    # ==========================================
    # TEMPLATE INTELLIGENCE
    # ==========================================

    composition_notes = ""

    if template_data:

        composition_notes = f"""

        TEMPLATE INTELLIGENCE:

        Product Zone:
        {template_data.get("product_zone")}

        Scene Intelligence:
        {template_data.get("scene_intelligence")}

        Style:
        {template_data.get("style")}

        Lighting:
        {template_data.get("lighting")}

        Composition:
        {template_data.get("composition_type")}

        """
    

    # ==========================================
    # FINAL PROMPT
    # ==========================================

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

    {composition_notes}

    REQUIREMENTS:

    - cinematic luxury advertising
    - realistic product placement
    - realistic shadows
    - elegant depth
    - premium commercial photography
    - modern wellness branding
    - award-winning advertising
    - clean typography hierarchy
    - luxury composition
    - realistic lighting
    - ultra aesthetic
    - high-end campaign design

    """

    # ==========================================
    # GEMINI IMAGE GENERATION
    # ==========================================

    response = client.models.generate_content(

        model=
        "gemini-2.0-flash-preview-image-generation",

        contents=prompt,

        config=types.GenerateContentConfig(

            response_modalities=[
                "TEXT",
                "IMAGE"
            ]
        )
    )


    # ==========================================
    # SAVE IMAGE
    # ==========================================

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


    # ==========================================
    # EXTRACT GENERATED IMAGE
    # ==========================================

    for part in response.candidates[0].content.parts:

        if part.inline_data:

            image_bytes = (
                part.inline_data.data
            )

            with open(

                output_path,

                "wb"
            ) as f:

                f.write(image_bytes)

            return {

                "local_path":
                output_path,

                "frontend_path":
                "/outputs/generated_ai_creative.png"
            }

    return None