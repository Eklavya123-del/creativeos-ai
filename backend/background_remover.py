# background_remover.py

from rembg import remove
from PIL import Image
import os


def remove_product_background(
    input_path,
    output_path
):

    with open(input_path, "rb") as f:
        input_data = f.read()

    output_data = remove(input_data)

    with open(output_path, "wb") as f:
        f.write(output_data)

    return output_path