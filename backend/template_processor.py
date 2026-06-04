from PIL import Image
import os
import json


RATIOS = {
    "square": (1, 1),
    "story": (9, 16),
    "feed": (4, 5),
    "banner": (16, 9)
}


def crop_to_ratio(image, ratio_w, ratio_h):

    width, height = image.size

    target_ratio = ratio_w / ratio_h
    current_ratio = width / height

    if current_ratio > target_ratio:

        new_width = int(
            height * target_ratio
        )

        left = (
            width - new_width
        ) // 2

        return image.crop(
            (
                left,
                0,
                left + new_width,
                height
            )
        )

    else:

        new_height = int(
            width / target_ratio
        )

        top = (
            height - new_height
        ) // 2

        return image.crop(
            (
                0,
                top,
                width,
                top + new_height
            )
        )


def process_template(
    template_path,
    template_name,
    template_dir,
    template_data_dir
):

    image = Image.open(
        template_path
    )

    for ratio_name, ratio in RATIOS.items():

        ratio_w, ratio_h = ratio

        cropped = crop_to_ratio(
            image.copy(),
            ratio_w,
            ratio_h
        )

        ratio_folder = os.path.join(
            template_dir,
            ratio_name
        )

        os.makedirs(
            ratio_folder,
            exist_ok=True
        )

        output_image = os.path.join(
            ratio_folder,
            template_name
        )

        cropped.save(
            output_image
        )

        # ------------------
        # JSON Metadata
        # ------------------

        json_folder = os.path.join(
            template_data_dir,
            ratio_name
        )

        os.makedirs(
            json_folder,
            exist_ok=True
        )

        json_path = os.path.join(
            json_folder,
            f"{os.path.splitext(template_name)[0]}.json"
        )

        metadata = {

            "scene_intelligence": {
                "scene_type": "premium podium",
                "product_type": "supplement bottle"
            },

            "placement": {
                "product_x": 0.50,
                "product_y": 0.42,
                "product_scale": 0.50
            },

            "lighting": "cinematic lighting",

            "composition_type":
            "premium product advertisement",

            "style":
            "luxury wellness"
        }

        with open(
            json_path,
            "w"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4
            )