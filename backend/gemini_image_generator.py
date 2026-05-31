
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
from google import genai
from google.genai import types

from PIL import Image
from io import BytesIO


client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)


def generate_creative_image(

    prompt: str
):

    try:

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

        output_dir = "../outputs"

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        generated_path = os.path.join(

            output_dir,

            f"{uuid.uuid4()}.png"
        )

        for part in response.candidates[0].content.parts:

            if part.inline_data:

                image = Image.open(

                    BytesIO(
                        part.inline_data.data
                    )
                )

                image.save(
                    generated_path
                )

                return generated_path

        return None

    except Exception as e:

        print(
            "IMAGE GENERATION ERROR:"
        )

        print(str(e))

        return None

