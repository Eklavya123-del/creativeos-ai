
import os

import google.generativeai as genai

from dotenv import load_dotenv

from creative_memory import (
    retrieve_similar_creatives,
    save_generation
)

# -----------------------------------
# LOAD ENV
# -----------------------------------
load_dotenv()

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

# -----------------------------------
# GEMINI MODEL
# -----------------------------------
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# -----------------------------------
# MAIN PROMPT GENERATOR
# -----------------------------------
def generate_nano_banana_prompt(

    campaign,

    style,

    ratio,

    template_data,

    selected_products
):

    # -----------------------------------
    # MEMORY RETRIEVAL
    # -----------------------------------
    memory = retrieve_similar_creatives(
        campaign
    )

    previous_creatives = ""

    try:

        previous_creatives = memory[
            "documents"
        ][0]

    except:

        previous_creatives = ""

    # -----------------------------------
    # TEMPLATE INTELLIGENCE
    # -----------------------------------
    scene = template_data.get(
        "scene_intelligence",
        {}
    )

    scene_type = scene.get(
        "scene_type",
        "premium podium"
    )

    visual_weight = scene.get(
        "visual_weight",
        "balanced"
    )

    lighting = template_data.get(
        "lighting",
        "soft cinematic lighting"
    )

    composition_type = template_data.get(
        "composition_type",
        "editorial wellness composition"
    )

    style_reference = template_data.get(
        "style",
        "luxury wellness"
    )

    # -----------------------------------
    # FINAL PROMPT
    # -----------------------------------
    prompt = f"""
    Create a premium cinematic wellness
    advertisement scene.

    CAMPAIGN:
    {campaign}

    STYLE:
    {style}

    OUTPUT RATIO:
    {ratio}

    PRODUCTS:
    {selected_products}

    CREATIVE DIRECTION:
    - Scene Type: {scene_type}
    - Lighting: {lighting}
    - Composition:
      {composition_type}
    - Visual Weight:
      {visual_weight}
    - Style:
      {style_reference}

    PREVIOUS SUCCESSFUL
    CREATIVE REFERENCES:
    {previous_creatives}

    REQUIREMENTS:
    - luxury wellness branding
    - realistic commercial photography
    - cinematic lighting
    - premium supplement advertising
    - shallow depth of field
    - elegant negative space
    - realistic shadows
    - modern editorial composition
    - ultra premium aesthetic
    - instagram advertisement quality
    - clean typography space
    - highly realistic

    Generate ONLY the final
    cinematic image generation prompt.
    """

    # -----------------------------------
    # GEMINI RESPONSE
    # -----------------------------------
    response = model.generate_content(
        prompt
    )

    final_prompt = response.text

    # -----------------------------------
    # SAVE TO MEMORY
    # -----------------------------------
    save_generation(

        campaign=campaign,

        style=style,

        ratio=ratio,

        template=scene_type,

        product=", ".join(
            selected_products
        ),

        final_prompt=final_prompt
    )

    return final_prompt

