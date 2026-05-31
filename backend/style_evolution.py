def get_style_modifiers(style):

    styles = {

        "premium": {
            "shadow_blur": 40,
            "product_scale": 0.92,
            "headline_size_boost": 8,
            "cta_radius": 40
        },

        "minimal": {
            "shadow_blur": 12,
            "product_scale": 0.78,
            "headline_size_boost": -4,
            "cta_radius": 18
        },

        "cinematic": {
            "shadow_blur": 55,
            "product_scale": 0.95,
            "headline_size_boost": 10,
            "cta_radius": 32
        },

        "scientific": {
            "shadow_blur": 20,
            "product_scale": 0.82,
            "headline_size_boost": 0,
            "cta_radius": 12
        }
    }

    return styles.get(
        style,
        styles["premium"]
    )