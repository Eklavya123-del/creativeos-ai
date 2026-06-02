import os
import requests

from dotenv import load_dotenv

load_dotenv()
# ==========================================
# ENV VARIABLES
# ==========================================

STABILITY_API_KEY = os.getenv(
    "STABILITY_API_KEY"
)


# ==========================================
# VALIDATE API KEY
# ==========================================

if not STABILITY_API_KEY:

    raise ValueError(
        "STABILITY_API_KEY not found in environment variables"
    )


# ==========================================
# MAIN GENERATION FUNCTION
# ==========================================

def generate_stability_creative(

    campaign_brief: str,

    headline: str,

    template_style: str,

    ratio: str,

    product_name: str,

    template_data: dict = None
):

    try:

        # ======================================
        # RATIO MAP
        # ======================================

        ratio_map = {

            "story": "9:16",

            "square": "1:1",

            "feed": "4:5",

            "banner": "16:9"
        }

        aspect_ratio = ratio_map.get(
            ratio,
            "1:1"
        )


        # ======================================
        # TEMPLATE INTELLIGENCE
        # ======================================

        template_context = ""

        if template_data:

            template_context = f"""

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
        

        # ======================================
        # FINAL PROMPT
        # ======================================

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

        {template_context}

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
        - social media campaign quality
        - highly realistic product photography

        """


        # ======================================
        # STABILITY API REQUEST
        # ======================================

        response = requests.post(

            "https://api.stability.ai/v2beta/stable-image/generate/core",

            headers={

                "Authorization":
                f"Bearer {STABILITY_API_KEY}",

                "Accept":
                "image/*"
            },

            files={

                "none": ("", "")
            },

            data={

                "prompt":
                prompt,

                "aspect_ratio":
                aspect_ratio,

                "output_format":
                "png"
            },

            timeout=120
        )


        # ======================================
        # ERROR HANDLING
        # ======================================

        if response.status_code != 200:

            raise Exception(

                f"Stability API Error: "
                f"{response.status_code} "
                f"{response.text}"
            )


        # ======================================
        # OUTPUT DIRECTORY
        # ======================================

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        output_dir = os.path.join(

            base_dir,

            "outputs"
        )

        os.makedirs(

            output_dir,

            exist_ok=True
        )


        # ======================================
        # SAVE IMAGE
        # ======================================

        output_path = os.path.join(

            output_dir,

            "generated_ai_creative.png"
        )

        with open(

            output_path,

            "wb"
        ) as file:

            file.write(response.content)


        # ======================================
        # RETURN FRONTEND PATH
        # ======================================

        return "/outputs/generated_ai_creative.png"

    except Exception as e:

        print(
            "IMAGE GENERATION ERROR:",
            str(e)
        )

        return None