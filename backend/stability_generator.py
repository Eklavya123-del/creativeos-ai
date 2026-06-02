import os
import requests

from dotenv import load_dotenv

load_dotenv()

STABILITY_API_KEY = os.getenv(
    "STABILITY_API_KEY"
)

# ======================================
# GENERATE CREATIVE
# ======================================

def generate_stability_creative(

    prompt,
    product_image_path,
    template_image_path,
    ratio="1:1"

):

    try:

        if not STABILITY_API_KEY:

            print(
                "STABILITY_API_KEY missing"
            )

            return None

        # ======================================
        # OPEN PRODUCT IMAGE
        # ======================================

        with open(
            product_image_path,
            "rb"
        ) as product_file:

            response = requests.post(

                "https://api.stability.ai/v2beta/stable-image/generate/sd3",

                headers={

                    "authorization":
                    f"Bearer {STABILITY_API_KEY}",

                    "accept":
                    "image/*"
                },

                files={

                    "image": (
                        os.path.basename(
                            product_image_path
                        ),
                        product_file,
                        "image/png"
                    )
                },

                data={

                    "prompt": f"""

                    {prompt}

                    IMPORTANT:

                    Use the uploaded product
                    image as the exact product.

                    Preserve:
                    - exact bottle
                    - exact supplement label
                    - exact packaging
                    - exact product colors

                    Generate:
                    - premium wellness advertisement
                    - cinematic composition
                    - realistic podium placement
                    - realistic shadows
                    - luxury lighting
                    - elegant reflections
                    - editorial commercial quality
                    - premium typography space
                    - instagram ad quality

                    Template reference:
                    {os.path.basename(template_image_path)}
                    """,

                    "strength": 0.95,

                    "aspect_ratio": ratio,

                    "output_format": "png"
                }
            )

        # ======================================
        # ERROR
        # ======================================

        if response.status_code != 200:

            print(
                "STABILITY ERROR:"
            )

            print(
                response.text
            )

            return None

        # ======================================
        # OUTPUT DIRECTORY
        # ======================================

        output_dir = os.path.join(

            os.path.dirname(__file__),

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

            file.write(
                response.content
            )

        # ======================================
        # RETURN WEB PATH
        # ======================================

        return (
            "/outputs/generated_ai_creative.png"
        )

    except Exception as e:

        print(
            "STABILITY GENERATION ERROR:"
        )

        print(str(e))

        return None