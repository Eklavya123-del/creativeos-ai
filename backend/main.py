
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.responses import (
    FileResponse
)
from gemini_image_generator import (
    generate_creative_image
)
from fastapi.staticfiles import (
    StaticFiles
)

from PIL import Image

from dotenv import load_dotenv

from pydantic import BaseModel

import chromadb

import google.generativeai as genai

import shutil
import os
import json
import uuid

from template_analyzer import (
    analyze_template
)

from nano_banana import (
    generate_nano_banana_prompt
)


# -----------------------------------
# LOAD ENV
# -----------------------------------
load_dotenv()


# -----------------------------------
# GEMINI
# -----------------------------------
genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# -----------------------------------
# CHROMA DB
# -----------------------------------
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = (
    chroma_client.get_or_create_collection(
        name="brand_creatives"
    )
)


# -----------------------------------
# FASTAPI
# -----------------------------------
app = FastAPI()


# -----------------------------------
# STATIC FILES
# -----------------------------------

os.makedirs(
    "outputs",
    exist_ok=True
)

os.makedirs(
    "uploads",
    exist_ok=True
)


app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.mount(
    "/templates",
    StaticFiles(directory="templates"),
    name="templates"
)


app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs"
)


# -----------------------------------
# CORS
# -----------------------------------
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# -----------------------------------
# PATHS
# -----------------------------------
UPLOAD_DIR = "/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# -----------------------------------
# MODELS
# -----------------------------------
class CampaignRequest(BaseModel):

    campaign: str


# -----------------------------------
# SAFE GEMINI
# -----------------------------------
def safe_generate(prompt):

    try:

        response = model.generate_content(
            prompt
        )

        if hasattr(response, "text"):

            return response.text

        return "AI response unavailable."

    except Exception as e:

        print("GEMINI ERROR:")
        print(str(e))

        return (
            "Creative intelligence "
            "temporarily unavailable."
        )


# -----------------------------------
# HOME
# -----------------------------------
@app.get("/")
def home():

    return {
        "message":
        "CreativeOS Backend Running"
    }


# -----------------------------------
# PRODUCTS API
# -----------------------------------
@app.get("/products")
def get_products():

    products_dir = os.path.join(

        "uploads",

        "products"
    )

    if not os.path.exists(
        products_dir
    ):

        return {
            "products": []
        }

    files = [

        file

        for file in os.listdir(
            products_dir
        )

        if file.endswith((
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        ))
    ]

    return {

        "products": files
    }


# -----------------------------------
# TEMPLATE LIST API
# -----------------------------------
@app.get("/template-list/{ratio}")
def get_templates(

    ratio: str
):

    template_dir = os.path.join(


        "templates",

        ratio
    )

    if not os.path.exists(
        template_dir
    ):

        return {
            "templates": []
        }

    templates = [

        file

        for file in os.listdir(
            template_dir
        )

        if file.endswith(".png")
    ]

    return {

        "templates": templates
    }


# -----------------------------------
# IMAGE UPLOAD
# -----------------------------------
@app.post("/upload")
async def upload_image(

    file: UploadFile = File(...)
):

    file_path = os.path.join(

        UPLOAD_DIR,

        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {

        "filename":
        file.filename,

        "path":
        file_path
    }


@app.post("/upload-product")
async def upload_product(

    file: UploadFile = File(...)
):

    save_dir = os.path.join(


        "uploads",

        "products"
    )

    os.makedirs(
        save_dir,
        exist_ok=True
    )

    file_path = os.path.join(

        save_dir,

        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {

        "status": "success",

        "filename":
        file.filename
    }

@app.post("/upload-template")
async def upload_template(

    ratio: str = Form(...),

    file: UploadFile = File(...)
):

    save_dir = os.path.join(


        "templates",

        ratio
    )

    os.makedirs(
        save_dir,
        exist_ok=True
    )

    file_path = os.path.join(

        save_dir,

        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # -----------------------------------
    # AUTO CREATE JSON
    # -----------------------------------
    json_dir = os.path.join(


        "template_data",

        ratio
    )

    os.makedirs(
        json_dir,
        exist_ok=True
    )

    json_path = os.path.join(

        json_dir,

        f"{os.path.splitext(file.filename)[0]}.json"
    )

    default_json = {

        "product_zone": {

            "x1": 250,
            "y1": 580,
            "x2": 750,
            "y2": 780
        },

        "scene_intelligence": {

            "anchor_surface": {

                "x1": 370,
                "y1": 760,
                "x2": 930,
                "y2": 790
            },

            "scene_type":
            "podium_showcase",

            "product_type":
            "bottle"
        }
    }

    with open(
        json_path,
        "w"
    ) as f:

        json.dump(
            default_json,
            f,
            indent=4
        )

    return {

        "status": "success",

        "template":
        file.filename
    }



# -----------------------------------
# GEMINI TEST
# -----------------------------------
@app.get("/test-gemini")
def test_gemini():

    response = safe_generate(
        "Say CreativeOS AI is working."
    )

    return {

        "response":
        response
    }


# -----------------------------------
# BRAND ANALYSIS
# -----------------------------------
@app.post("/analyze-brand")
async def analyze_brand(

    file: UploadFile = File(...)
):

    image = Image.open(
        file.file
    )

    prompt = """
    You are a premium wellness
    creative strategist.

    Analyze this brand creative.

    Generate:
    - brand tone
    - visual identity
    - luxury positioning
    - aesthetic direction
    """

    response = safe_generate(prompt)

    collection.add(

        documents=[response],

        ids=[file.filename]
    )

    return {

        "analysis":
        response
    }


# -----------------------------------
# RETRIEVE MEMORY
# -----------------------------------
@app.get("/retrieve")
def retrieve(query: str):

    try:

        results = collection.query(

            query_texts=[query],

            n_results=5
        )

        return results

    except Exception as e:

        return {
            "error": str(e)
        }


# -----------------------------------
# GENERATE COPY
# -----------------------------------
@app.post("/generate-copy")
def generate_copy(

    data: CampaignRequest
):

    query = data.campaign

    references = []

    try:

        results = collection.query(

            query_texts=[query],

            n_results=3
        )

        references = (
            results["documents"][0]
        )

    except Exception as e:

        print(str(e))

    prompt = f"""
    You are an AI creative
    strategist for a premium
    wellness brand.

    Campaign:
    {query}

    Previous References:
    {references}

    Generate:

    1. 5 Headlines
    2. 5 CTA Variations
    3. 3 Ad Copy Variations

    Keep it:
    cinematic,
    premium,
    luxury,
    scientific,
    wellness-focused.
    """

    response = safe_generate(
        prompt
    )

    return {

        "campaign":
        query,

        "references":
        references,

        "generated_copy":
        response
    }


# -----------------------------------
# ANALYZE TEMPLATE
# -----------------------------------
@app.post("/analyze-template")
def analyze_template_route(

    template_name: str,

    ratio: str
):

    template_path = os.path.join(

        ratio,

        template_name
    )

    data = analyze_template(

        template_path,

        model
    )

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    save_dir = os.path.join(

        BASE_DIR,

        "template_data",

        ratio
    )

    os.makedirs(

        save_dir,

        exist_ok=True
    )

    save_path = os.path.join(

        save_dir,

        f"{template_name}.json"
    )

    with open(
        save_path,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )

    return data


# -----------------------------------
# AI CREATIVE GENERATION
# -----------------------------------

@app.post("/generate-ai-creative")
def generate_ai_creative(

    campaign: str = Form(...),

    style: str = Form(...),

    ratio: str = Form(...),

    template_name: str = Form(...),

    selected_products: str = Form(...)
):

    try:

        # -----------------------------------
        # TEMPLATE JSON
        # -----------------------------------
        template_json_path = os.path.join(


            "template_data",

            ratio,

            f"{os.path.splitext(template_name)[0]}.json"
        )

        with open(
            template_json_path,
            "r"
        ) as f:

            template_data = json.load(f)

        # -----------------------------------
        # PRODUCTS
        # -----------------------------------
        products = [

            p.strip()

            for p in selected_products.split(",")

            if p.strip()
        ]

        # -----------------------------------
        # CREATIVE MEMORY
        # -----------------------------------
        references = []

        try:

            memory_results = collection.query(

                query_texts=[campaign],

                n_results=3
            )

            if (
                memory_results and
                memory_results["documents"]
            ):

                references = (
                    memory_results["documents"][0]
                )

        except Exception as e:

            print("MEMORY ERROR:")
            print(str(e))

        # -----------------------------------
        # FINAL MASTER PROMPT
        # -----------------------------------
        final_prompt = (
            generate_nano_banana_prompt(

                campaign=campaign,

                style=style,

                ratio=ratio,

                template_data=template_data,

                selected_products=products,

                references=references
            )
        )

        # -----------------------------------
        # CREATIVE DIRECTIONS
        # -----------------------------------
        directions = [

            "Balanced",

            "Cinematic",

            "Editorial",

            "Bold"
        ]

        variants = []

        for direction in directions:

            # -----------------------------------
            # VARIANT PROMPT
            # -----------------------------------
            variant_prompt = f"""

            Create a premium luxury
            wellness advertisement.

            Campaign:
            {campaign}

            Style:
            {style}

            Creative Direction:
            {direction}

            Ratio:
            {ratio}

            Products:
            {products}

            Template Intelligence:
            {template_data}

            Previous Creative Memory:
            {references}

            MASTER PROMPT:
            {final_prompt}

            REQUIREMENTS:

            - luxury wellness aesthetic
            - cinematic lighting
            - premium typography
            - realistic product placement
            - modern advertising feel
            - high-end composition
            - ultra realistic
            - premium skincare/wellness campaign
            - realistic shadows
            - realistic reflections
            - cinematic atmosphere
            - elegant composition
            - expensive looking
            - professional advertising photography

            IMPORTANT:
            Make the creative look like
            an award-winning wellness ad campaign.
            """

            # -----------------------------------
            # AI DESCRIPTION
            # -----------------------------------
            description = safe_generate(

                f"""
                You are an elite creative
                director for luxury wellness
                campaigns.

                Analyze this direction:

                {variant_prompt}

                Generate:
                - visual strategy
                - lighting style
                - composition logic
                - emotional tone
                - premium campaign reasoning

                Keep it concise,
                cinematic and premium.
                """
            )

            # -----------------------------------
            # REAL IMAGE GENERATION
            # -----------------------------------
            generated_image = (
                generate_creative_image(
                    variant_prompt
                )
            )

            # -----------------------------------
            # FALLBACK
            # -----------------------------------

                
            image_path = (

                    generated_image

                    if generated_image

                    else
                    f"templates/{ratio}/{template_name}"
            )



            # -----------------------------------
            # VARIANT
            # -----------------------------------
            variants.append({

                "name":
                direction,

                "image":
                image_path,

                "prompt":
                variant_prompt,

                "description":
                description
            })

        # -----------------------------------
        # AI STRATEGIST
        # -----------------------------------
        strategy_response = safe_generate(

            f"""
            You are a luxury wellness
            creative strategist.

            Campaign:
            {campaign}

            Style:
            {style}

            Products:
            {products}

            Template:
            {template_name}

            Previous Creative Memory:
            {references}

            Generate:

            1. Premium headline
            2. Luxury CTA
            3. Brand positioning
            4. Emotional direction
            5. Creative strategy summary

            Keep it cinematic,
            premium, modern,
            concise and elegant.
            """
        )

        # -----------------------------------
        # STORE MEMORY
        # -----------------------------------
        try:

            collection.add(

                documents=[

                    f"""
                    Campaign:
                    {campaign}

                    Style:
                    {style}

                    Template:
                    {template_name}

                    Strategy:
                    {strategy_response}
                    """
                ],

                ids=[str(uuid.uuid4())]
            )

        except Exception as e:

            print(
                "MEMORY STORE ERROR:"
            )

            print(str(e))

        # -----------------------------------
        # RESPONSE
        # -----------------------------------
        return {

            "status": "success",

            "campaign":
            campaign,

            "variants":
            variants,

            "strategy":
            strategy_response
        }

    except Exception as e:

        print(
            "AI GENERATION ERROR:"
        )

        print(str(e))

        return {

            "status": "error",

            "variants": [],

            "strategy":
            "Creative generation failed.",

            "error": str(e)
        }



# -----------------------------------
# GENERATED IMAGE
# -----------------------------------
@app.get("/generated-image")
def get_generated_image():

    return FileResponse(

        "/outputs/square_cinematic_generated_ad.png"
    )

