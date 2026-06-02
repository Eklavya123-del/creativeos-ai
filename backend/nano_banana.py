import os

import google.generativeai as genai

from dotenv import load_dotenv

from creative_memory import (
    retrieve_similar_creatives,
    save_generation
)

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

genai.configure(

    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

# ==========================================
# GEMINI MODEL
# ==========================================

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================================
# MAIN PROMPT GENERATOR
# ==========================================

def generate_nano_banana_prompt(

    campaign,

    style,

    ratio,

    template_data,

    selected_products
):

    try:

        # ======================================
        # MEMORY RETRIEVAL
        # ======================================

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


        # ======================================
        # TEMPLATE INTELLIGENCE
        # ======================================

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

        product_type = scene.get(
            "product_type",
            "supplement bottle"
        )


        # ======================================
        # PRODUCT STRING
        # ======================================

        if isinstance(
            selected_products,
            list
        ):

            product_string = ", ".join(
                selected_products
            )

        else:

            product_string = str(
                selected_products
            )


        # ======================================
        # RATIO GUIDANCE
        # ======================================

        ratio_guidance = {

            "story":
            "vertical mobile advertisement composition",

            "square":
            "balanced instagram advertisement composition",

            "feed":
            "social media editorial composition",

            "banner":
            "wide cinematic advertising composition"
        }

        ratio_context = ratio_guidance.get(
            ratio,
            "premium advertisement composition"
        )


        # ======================================
        # FINAL PROMPT
        # ======================================

        prompt = f"""

        Create a premium cinematic wellness
        supplement advertisement.

        CAMPAIGN:
        {campaign}

        STYLE:
        {style}

        OUTPUT FORMAT:
        {ratio_context}

        PRODUCTS:
        {product_string}

        PRODUCT TYPE:
        {product_type}

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
        - cinematic commercial photography
        - realistic supplement advertising
        - elegant composition
        - premium shadows
        - realistic lighting
        - editorial photography style
        - clean negative space
        - modern wellness marketing
        - shallow depth of field
        - realistic product placement
        - luxury instagram campaign
        - highly aesthetic
        - award-winning ad quality
        - realistic premium materials
        - commercial product photography

        IMPORTANT:
        Generate ONLY the final
        cinematic image generation prompt.

        Do NOT explain anything.

        """


        # ======================================
        # GEMINI RESPONSE
        # ======================================

        response = model.generate_content(
            prompt
        )

        final_prompt = (
            response.text.strip()
        )


        # ======================================
        # SAVE TO MEMORY
        # ======================================

        save_generation(

            campaign=campaign,

            style=style,

            ratio=ratio,

            template=scene_type,

            product=product_string,

            final_prompt=final_prompt
        )


        # ======================================
        # RETURN FINAL PROMPT
        # ======================================

        return final_prompt


    except Exception as e:

        print(
            "NANO BANANA ERROR:",
            str(e)
        )

        return f"""

        Premium cinematic wellness
        supplement advertisement.

        Campaign:
        {campaign}

        Style:
        {style}

        Product:
        {selected_products}

        Luxury wellness branding.
        Cinematic commercial lighting.
        Realistic supplement photography.
        Premium composition.
        Elegant shadows.
        Editorial campaign aesthetic.
        Modern instagram advertisement.
        Highly realistic.
        """