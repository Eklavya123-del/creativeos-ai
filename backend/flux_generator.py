
import os
import uuid
import replicate
import requests

from dotenv import load_dotenv


# -----------------------------------
# LOAD .ENV FROM BACKEND DIRECTORY
# -----------------------------------
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

env_path = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(env_path)


# -----------------------------------
# DEBUG TOKEN
# -----------------------------------
replicate_token = os.getenv(
    "REPLICATE_API_TOKEN"
)

print(
    "REPLICATE TOKEN:",
    replicate_token
)


# -----------------------------------
# VALIDATE TOKEN
# -----------------------------------
if not replicate_token:

    raise ValueError(
        "REPLICATE_API_TOKEN missing from .env"
    )


os.environ[
    "REPLICATE_API_TOKEN"
] = replicate_token


# -----------------------------------
# IMAGE GENERATION
# -----------------------------------
def generate_flux_image(

    prompt
):

    output = replicate.run(

        "black-forest-labs/flux-schnell",

        input={

            "prompt": prompt,

            "aspect_ratio": "1:1",

            "output_format": "png",

            "output_quality": 100
        }
    )

    image_url = output[0]

    response = requests.get(
        image_url
    )

    output_dir = os.path.join(
        "..",
        "outputs"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    unique_id = str(
        uuid.uuid4()
    )[:8]

    output_path = os.path.join(

        output_dir,

        f"flux_{unique_id}.png"
    )

    with open(
        output_path,
        "wb"
    ) as f:

        f.write(
            response.content
        )

    return output_path

