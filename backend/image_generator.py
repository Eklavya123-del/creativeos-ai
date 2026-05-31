
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter,
    ImageOps
)

import json
import os
import textwrap
import uuid


# -----------------------------------
# TEXT WRAPPING
# -----------------------------------
def wrap_text(
    text,
    max_chars_per_line=18
):

    lines = textwrap.wrap(
        text,
        width=max_chars_per_line
    )

    return "\n".join(lines)


# -----------------------------------
# CINEMATIC VIGNETTE
# -----------------------------------
def apply_vignette(image):

    width, height = image.size

    vignette = Image.new(
        "L",
        (width, height),
        255
    )

    draw = ImageDraw.Draw(vignette)

    draw.ellipse(
        (
            150,
            100,
            width - 150,
            height - 100
        ),
        fill=0
    )

    vignette = vignette.filter(
        ImageFilter.GaussianBlur(180)
    )

    black_layer = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 110)
    )

    black_layer.putalpha(vignette)

    return Image.alpha_composite(
        image,
        black_layer
    )


# -----------------------------------
# MAIN GENERATION FUNCTION
# -----------------------------------
def generate_ad(
    headline,
    cta,
    product_image_path,
    template_name,
    ratio,
    style="premium",
    variant_data=None
):

    # -----------------------------------
    # BASE DIRECTORY
    # -----------------------------------
    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    # -----------------------------------
    # LOAD TEMPLATE JSON
    # -----------------------------------
    json_path = os.path.join(
        BASE_DIR,
        "..",
        "template_data",
        ratio,
        f"{template_name}.json"
    )

    with open(json_path, "r") as f:

        template_data = json.load(f)

    # -----------------------------------
    # TEMPLATE PROFILE
    # -----------------------------------
    profile = template_data[
        "template_profile"
    ]

    # -----------------------------------
    # LOAD TEMPLATE IMAGE
    # -----------------------------------
    template_path = os.path.join(
        BASE_DIR,
        "..",
        "templates",
        ratio,
        template_name
    )

    template = Image.open(
        template_path
    ).convert("RGBA")

    # -----------------------------------
    # LOAD PRODUCT IMAGE
    # -----------------------------------
    product_path = os.path.join(
        BASE_DIR,
        "..",
        "uploads",
        product_image_path
    )

    product = Image.open(
        product_path
    ).convert("RGBA")

    # -----------------------------------
    # REMOVE TRANSPARENT MARGINS
    # -----------------------------------
    bbox = product.getbbox()

    if bbox:

        product = product.crop(bbox)

    # -----------------------------------
    # TEMPLATE ZONES
    # -----------------------------------
    PRODUCT_AREA = template_data[
        "product_zone"
    ]

    HEADLINE_ZONE = template_data[
        "headline_zone"
    ]

    CTA_ZONE = template_data[
        "cta_zone"
    ]

    SCENE = template_data[
        "scene_intelligence"
    ]

    # -----------------------------------
    # PRODUCT DIMENSIONS
    # -----------------------------------
    product_width, product_height = product.size

    area_width = (
        PRODUCT_AREA["x2"] -
        PRODUCT_AREA["x1"]
    )

    area_height = (
        PRODUCT_AREA["y2"] -
        PRODUCT_AREA["y1"]
    )

    # -----------------------------------
    # BASE SCALE
    # -----------------------------------
    scale_ratio = min(
        area_width / product_width,
        area_height / product_height
    )

    # -----------------------------------
    # TEMPLATE PROFILE SCALE
    # -----------------------------------
    recommended_scale = profile.get(
        "recommended_product_scale",
        0.78
    )

    scale_ratio *= recommended_scale

    # -----------------------------------
    # VARIANT SCALE
    # -----------------------------------
    if variant_data:

        scale_ratio *= variant_data.get(
            "product_scale",
            1.0
        )

    # -----------------------------------
    # FINAL PRODUCT SIZE
    # -----------------------------------
    new_width = int(
        product_width * scale_ratio
    )

    new_height = int(
        product_height * scale_ratio
    )

    # -----------------------------------
    # PRODUCT HEIGHT CLAMP
    # -----------------------------------
    max_product_height = int(
        template.height * 0.42
    )

    if new_height > max_product_height:

        resize_ratio = (
            max_product_height /
            new_height
        )

        new_width = int(
            new_width *
            resize_ratio
        )

        new_height = max_product_height

    # -----------------------------------
    # RESIZE PRODUCT
    # -----------------------------------
    product = product.resize(
        (new_width, new_height)
    )

    # -----------------------------------
    # ANCHOR SURFACE
    # -----------------------------------
    anchor = SCENE[
        "anchor_surface"
    ]

    # -----------------------------------
    # PRODUCT POSITIONING
    # -----------------------------------
    anchor_center_x = (
        anchor["x1"] +
        anchor["x2"]
    ) // 2

    paste_x = (
        anchor_center_x -
        new_width // 2
    )

    # -----------------------------------
    # OPTICAL OFFSET
    # -----------------------------------
    paste_x -= 12

    # -----------------------------------
    # SAFE MARGINS
    # -----------------------------------
    paste_x = max(
        40,
        paste_x
    )

    # -----------------------------------
    # PRODUCT Y POSITION
    # -----------------------------------
    paste_y = (
        anchor["y1"]
        - new_height
        + 24
    )

    # -----------------------------------
    # VARIANT POSITION ADJUSTMENT
    # -----------------------------------
    if variant_data:

        paste_x += variant_data.get(
            "x_shift",
            0
        )

        paste_y += variant_data.get(
            "y_shift",
            0
        )

    # -----------------------------------
    # REALISTIC SHADOW
    # -----------------------------------
    alpha = product.split()[-1]

    shadow_blur = 24

    if variant_data:

        shadow_blur = variant_data.get(
            "shadow_blur",
            24
        )

    shadow = Image.new(
        "RGBA",
        product.size,
        (0, 0, 0, 100)
    )

    shadow.putalpha(alpha)

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(
            shadow_blur
        )
    )

    shadow_x = paste_x + 6

    shadow_y = (
        paste_y +
        new_height -
        18
    )

    template.paste(
        shadow,
        (shadow_x, shadow_y),
        shadow
    )

    # -----------------------------------
    # PRODUCT GLOW
    # -----------------------------------
    glow = Image.new(
        "RGBA",
        product.size,
        (255, 255, 255, 28)
    )

    glow.putalpha(alpha)

    glow = glow.filter(
        ImageFilter.GaussianBlur(40)
    )

    template.paste(
        glow,
        (paste_x, paste_y),
        glow
    )

    # -----------------------------------
    # PASTE PRODUCT
    # -----------------------------------
    template.paste(
        product,
        (paste_x, paste_y),
        product
    )

    # -----------------------------------
    # DRAW OBJECT
    # -----------------------------------
    draw = ImageDraw.Draw(template)

    # -----------------------------------
    # TYPOGRAPHY
    # -----------------------------------
    headline_font_size = profile.get(
        "recommended_headline_size",
        64
    )

    # -----------------------------------
    # VARIANT TYPOGRAPHY
    # -----------------------------------
    if variant_data:

        headline_font_size = int(
            headline_font_size *
            variant_data.get(
                "headline_scale",
                1.0
            )
        )

    # -----------------------------------
    # RESPONSIVE REDUCTION
    # -----------------------------------
    if len(headline) > 35:

        headline_font_size -= 6

    if len(headline) > 55:

        headline_font_size -= 10

    # -----------------------------------
    # LOAD FONTS
    # -----------------------------------
    try:

        font_path = os.path.join(
            BASE_DIR,
            "..",
            "fonts",
            "Montserrat-Bold.ttf"
        )

        headline_font = ImageFont.truetype(
            font_path,
            headline_font_size
        )

        cta_font = ImageFont.truetype(
            font_path,
            32
        )

    except Exception as e:

        print(
            "FONT ERROR:",
            e
        )

        headline_font = ImageFont.load_default()

        cta_font = ImageFont.load_default()

    # -----------------------------------
    # DYNAMIC WRAPPING
    # -----------------------------------
    safe_headline_length = profile.get(
        "safe_headline_length",
        32
    )

    max_chars = 18

    if safe_headline_length <= 24:

        max_chars = 14

    elif safe_headline_length >= 40:

        max_chars = 22

    wrapped_headline = wrap_text(
        headline,
        max_chars
    )

    # -----------------------------------
    # HEADLINE POSITION
    # -----------------------------------
    headline_x = HEADLINE_ZONE["x1"]

    headline_y = HEADLINE_ZONE["y1"]

    # -----------------------------------
    # DRAW HEADLINE
    # -----------------------------------
    draw.text(
        (headline_x, headline_y),
        wrapped_headline,
        fill=(10, 10, 10),
        font=headline_font,
        spacing=10
    )

    # -----------------------------------
    # CTA BUTTON
    # -----------------------------------
    draw.rounded_rectangle(
        (
            CTA_ZONE["x1"],
            CTA_ZONE["y1"],
            CTA_ZONE["x2"],
            CTA_ZONE["y2"]
        ),

        radius=26,

        fill=(25, 25, 25)
    )

    # -----------------------------------
    # CTA POSITION
    # -----------------------------------
    cta_text_x = CTA_ZONE["x1"] + 38

    cta_text_y = CTA_ZONE["y1"] + 20

    # -----------------------------------
    # DRAW CTA
    # -----------------------------------
    draw.text(
        (cta_text_x, cta_text_y),
        cta,
        fill=(240, 240, 240),
        font=cta_font
    )

    # -----------------------------------
    # CINEMATIC DEPTH
    # -----------------------------------
    background_blur = template.filter(
        ImageFilter.GaussianBlur(0.25)
    )

    template = Image.blend(
        background_blur,
        template,
        0.96
    )

    # -----------------------------------
    # APPLY VIGNETTE
    # -----------------------------------
    template = apply_vignette(
        template
    )

    # -----------------------------------
    # OUTPUT DIRECTORY
    # -----------------------------------
    output_dir = os.path.join(
        BASE_DIR,
        "..",
        "outputs"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    # -----------------------------------
    # UNIQUE FILE NAME
    # -----------------------------------
    unique_id = str(
        uuid.uuid4()
    )[:8]

    output_filename = (
        f"{ratio}_{style}_{unique_id}.png"
    )

    output_path = os.path.join(
        output_dir,
        output_filename
    )

    # -----------------------------------
    # SAVE OUTPUT
    # -----------------------------------
    template.save(output_path)

    print(
        f"Creative saved at: {output_path}"
    )

    return {

        "output_path":
            f"outputs/{output_filename}",

        "variant_data":
            variant_data
    }

