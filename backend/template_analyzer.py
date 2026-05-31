import google.generativeai as genai
from PIL import Image
import json
import os
def analyze_template(template_path, model):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    full_template_path = os.path.join(
        BASE_DIR,
        "..",
        "templates",
        template_path
    )
    print(full_template_path)
    image = Image.open(full_template_path)

    prompt = """
    Analyze this advertising template.

    Identify:

    1. Product placement zone
    2. Headline safe zone
    3. CTA safe zone
    4. Visual hierarchy
    5. Composition type
    6. Lighting direction
    7. Whitespace density
    8. Recommended product scale
    9. Aesthetic style
    10. Preferred text alignment

    Return ONLY valid JSON.

    Example:

    {
      "product_zone": {
        "x1": 500,
        "y1": 220,
        "x2": 980,
        "y2": 900
      },

      "headline_zone": {
        "x1": 80,
        "y1": 120,
        "x2": 480,
        "y2": 420
      },

      "cta_zone": {
        "x1": 80,
        "y1": 820,
        "x2": 350,
        "y2": 940
      },

      "composition_type": "floating cinematic",
      "lighting": "top-right soft lighting",
      "whitespace": "high",
      "recommended_product_scale": "medium-large",
      "style": "premium wellness cinematic",
      "text_alignment": "left"
    }
    """

    response = model.generate_content(
        [prompt, image]
    )

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)