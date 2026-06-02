import os
import requests
from dotenv import load_dotenv

load_dotenv()

STABILITY_API_KEY = os.getenv(
    "STABILITY_API_KEY"
)

if not STABILITY_API_KEY:

    raise ValueError(
        "STABILITY_API_KEY not found"
    )


def generate_stability_creative(
    prompt: str
):

    api_host = "https://api.stability.ai"

    engine_id = "stable-diffusion-xl-1024-v1-0"

    response = requests.post(

        f"{api_host}/v1/generation/{engine_id}/text-to-image",

        headers={

            "Content-Type":
            "application/json",

            "Accept":
            "application/json",

            "Authorization":
            f"Bearer {STABILITY_API_KEY}"
        },

        json={

            "text_prompts": [

                {
                    "text": prompt,
                    "weight": 1
                }
            ],

            "cfg_scale": 7,

            "height": 1024,

            "width": 1024,

            "samples": 1,

            "steps": 30
        }
    )

    if response.status_code != 200:

        raise Exception(
            f"Stability API Error: {response.text}"
        )

    data = response.json()

    image_base64 = data[
        "artifacts"
    ][0]["base64"]

    import base64

    image_bytes = base64.b64decode(
        image_base64
    )

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

        "square_cinematic_generated_ad.png"
    )

    with open(
        output_path,
        "wb"
    ) as f:

        f.write(image_bytes)

    return (
        "/outputs/square_cinematic_generated_ad.png"
    )