def get_product_behavior(
    product_type
):

    behaviors = {

        "bottle": {

            "scale_multiplier": 1.15,

            "shadow_intensity": 1.0,

            "preferred_alignment":
                "bottom-center",

            "headline_space":
                "left-heavy"
        },

        "jar": {

            "scale_multiplier": 1.28,

            "shadow_intensity": 1.2,

            "preferred_alignment":
                "center",

            "headline_space":
                "top-left"
        },

        "gummies": {

            "scale_multiplier": 1.4,

            "shadow_intensity": 0.8,

            "preferred_alignment":
                "floating-center",

            "headline_space":
                "top"
        },

        "sachet": {

            "scale_multiplier": 1.05,

            "shadow_intensity": 0.7,

            "preferred_alignment":
                "angled",

            "headline_space":
                "left"
        }
    }

    return behaviors.get(
        product_type,
        behaviors["bottle"]
    )