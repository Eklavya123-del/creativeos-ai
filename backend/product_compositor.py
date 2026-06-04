from PIL import Image
import os
from PIL import Image

from shadow_generator import (
    add_contact_shadow
)
def composite_product_on_scene(
    scene_path,
    product_path,
    output_path,
    scale=0.55,
    product_x=0.50,
    product_y=0.38
):
    """
    Places transparent product PNG
    on top of generated scene.
    """

    scene = Image.open(
        scene_path
    ).convert("RGBA")

    product = Image.open(
        product_path
    ).convert("RGBA")

    scene_width, scene_height = scene.size

    # -------------------------
    # Resize Product
    # -------------------------

    target_width = int(
        scene_width * scale
    )

    aspect_ratio = (
        product.height /
        product.width
    )

    target_height = int(
        target_width *
        aspect_ratio
    )

    product = product.resize(
        (
            target_width,
            target_height
        )
    )

    # -------------------------
    # Center Placement
    # -------------------------

    x = int(
    scene_width * product_x
    ) - (target_width // 2)

    y = int(
        scene_height * product_y
    )
    # -------------------------
    # Add Shadow
    # -------------------------

    scene = add_contact_shadow(
        scene,
        product,
        x,
        y
    )

    # -------------------------
    # Add Product
    # -------------------------

    scene.alpha_composite(
        product,
        (x, y)
    )

    scene.save(
        output_path,
        "PNG"
    )

    return output_path