
from image_generator import generate_ad

from layout_mutator import (
    generate_variants
)


def generate_variant_ads(
    headline,
    cta,
    product_image_path,
    template_name,
    ratio,
    style="premium"
):

    variants = generate_variants()

    outputs = []

    for variant in variants:

        result = generate_ad(

            headline=headline,

            cta=cta,

            product_image_path=product_image_path,

            template_name=template_name,

            ratio=ratio,

            style=style,

            variant_data=variant
        )

        outputs.append({

            "name": variant["name"],

            "image": result[
                "output_path"
            ],

            "variant_data": result[
                "variant_data"
            ]
        })

    return outputs

