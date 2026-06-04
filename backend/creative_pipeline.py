import os
import json

from background_remover import (
    remove_product_background
)

from stability_generator import (
    generate_stability_creative
)

from product_compositor import (
    composite_product_on_scene
)


def generate_final_creative(
    product_path,
    template_image_path,
    template_json_path,
    prompt,
    ratio
):

    # ====================================
    # OUTPUT DIR
    # ====================================

    output_dir = os.path.join(
        os.path.dirname(__file__),
        "outputs"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    # ====================================
    # STEP 1
    # REMOVE BACKGROUND
    # ====================================

    cutout_path = os.path.join(
        output_dir,
        "product_cutout.png"
    )

    remove_product_background(
        product_path,
        cutout_path
    )

    # ====================================
    # STEP 2
    # GENERATE SCENE
    # ====================================

    scene_result = (
        generate_stability_creative(
            prompt=prompt,
            product_image_path=product_path,
            template_image_path=template_image_path,
            ratio=ratio
        )
    )

    if not scene_result:

        return None

    scene_path = os.path.join(
        output_dir,
        "generated_ai_creative.png"
    )

    # ====================================
    # STEP 3
    # LOAD TEMPLATE JSON
    # ====================================

    placement = {

        "product_x": 0.50,
        "product_y": 0.34,
        "product_scale": 0.55
    }

    if os.path.exists(
        template_json_path
    ):

        with open(
            template_json_path,
            "r"
        ) as f:

            data = json.load(f)

            placement = data.get(
                "placement",
                placement
            )

    # ====================================
    # STEP 4
    # COMPOSITE PRODUCT
    # ====================================

    final_output = os.path.join(
        output_dir,
        "final_creative.png"
    )

    composite_product_on_scene(

    scene_path=scene_path,

    product_path=cutout_path,

    output_path=final_output,

    scale=placement.get(
        "product_scale",
        0.55
    ),

    product_x=placement.get(
        "product_x",
        0.50
    ),

    product_y=placement.get(
        "product_y",
        0.38
    )
)

    return "/outputs/final_creative.png"