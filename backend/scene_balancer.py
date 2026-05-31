
def get_scene_balance(scene):

    scene_type = scene.get(
        "scene_type",
        "default"
    )

    if scene_type == "podium_showcase":

        return {

            "product_scale": 1.15,

            "headline_scale": 1.2,

            "shadow_blur": 24,

            "depth_strength": 0.94
        }

    elif scene_type == "floating_hero":

        return {

            "product_scale": 1.02,

            "headline_scale": 1.1,

            "shadow_blur": 30,

            "depth_strength": 0.92
        }

    return {

        "product_scale": 1.2,

        "headline_scale": 1.0,

        "shadow_blur": 20,

        "depth_strength": 0.9
    }

