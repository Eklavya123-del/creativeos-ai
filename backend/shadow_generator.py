from PIL import (
    Image,
    ImageFilter,
    ImageEnhance
)


def add_contact_shadow(
    scene,
    product,
    x,
    y
):
    """
    Generates a realistic contact shadow
    beneath the product.
    """

    alpha = product.getchannel("A")

    shadow = Image.new(
        "RGBA",
        product.size,
        (0, 0, 0, 255)
    )

    shadow.putalpha(alpha)

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(30)
    )

    shadow_alpha = shadow.getchannel("A")

    shadow_alpha = (
        ImageEnhance.Brightness(
            shadow_alpha
        ).enhance(0.28)
    )

    shadow.putalpha(
        shadow_alpha
    )

    shadow_x = x

    shadow_y = y + int(
        product.height * 0.75
    )

    scene.alpha_composite(
        shadow,
        (shadow_x, shadow_y)
    )

    return scene