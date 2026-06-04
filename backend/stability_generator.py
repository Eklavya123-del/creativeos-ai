import os
import requests

from dotenv import load_dotenv

load_dotenv()

STABILITY_API_KEY = os.getenv(
    "STABILITY_API_KEY"
)


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

        response = requests.post(

            "https://api.stability.ai/v2beta/stable-image/generate/core",

            headers={

                "authorization":
                f"Bearer {STABILITY_API_KEY}",

                "accept":
                "image/*"
            },

            data={

                "prompt":
                f"""

                Create a premium cinematic
                wellness advertising environment.

                IMPORTANT:

                - DO NOT generate a product
                - DO NOT generate a bottle
                - Leave the podium empty
                - Leave the foreground clear
                - Create a luxury scene for
                  later hero product placement

                SCENE REQUIREMENTS:

                {prompt}

                - luxury podium

                - cinematic lighting

                - premium reflections

                - realistic shadows

                - luxury wellness branding

                - commercial photography

                - highly realistic

                - elegant composition

                - instagram luxury ad quality

                - premium materials

                - shallow depth of field

                """,

                "output_format":
                "png",

                "aspect_ratio":
                ratio
            }
        )

        if response.status_code != 200:

            print(
                "STABILITY ERROR:"
            )

            print(
                response.text
            )

            return None

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
        ) as file:

            file.write(
                response.content
            )

        return (
            "/outputs/generated_ai_creative.png"
        )

    except Exception as e:

        print(
            "STABILITY GENERATION ERROR:"
        )

        print(str(e))

        return None