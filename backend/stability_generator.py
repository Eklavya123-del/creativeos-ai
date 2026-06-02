import os
import requests
from dotenv import load_dotenv

load_dotenv()

STABILITY_API_KEY = os.getenv(
    "STABILITY_API_KEY"
)

# ======================================
# GENERATE IMAGE
# ======================================

def generate_stability_creative(prompt):

    if not STABILITY_API_KEY:

        print(
            "WARNING: STABILITY_API_KEY missing"
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

        files={

            "none":
            ""
        },

        data={

            "prompt":
            prompt,

            "output_format":
            "png"
        }
    )

    if response.status_code != 200:

        print(
            "STABILITY ERROR:",
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

        file.write(response.content)

    return "/outputs/generated_ai_creative.png"