from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.staticfiles import (
    StaticFiles
)

from fastapi.responses import (
    FileResponse
)

from pydantic import BaseModel

from PIL import Image

import google.generativeai as genai

from dotenv import load_dotenv

import chromadb

import shutil
import os
import json
import uuid

from gemini_image_generator import (
    generate_gemini_creative
)

# ============================================
# LOAD ENV
# ============================================

load_dotenv()

# ============================================
# PATHS
# ============================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)



UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs"
)

TEMPLATE_DIR = os.path.join(
    BASE_DIR,
    "templates"
)

TEMPLATE_DATA_DIR = os.path.join(
    BASE_DIR,
    "template_data"
)

CHROMA_DIR = os.path.join(
    BASE_DIR,
    "chroma_db"
)

FONT_DIR = os.path.join(
    BASE_DIR,
    "fonts"
)



os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

os.makedirs(
    os.path.join(
        UPLOAD_DIR,
        "products"
    ),
    exist_ok=True
)

# ============================================
# GEMINI
# ============================================

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ============================================
# CHROMA DB
# ============================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = chroma_client.get_or_create_collection(
    name="brand_creatives"
)

# ============================================
# FASTAPI
# ============================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ENSURE DIRECTORIES EXIST
# ============================================

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

os.makedirs(
    TEMPLATE_DIR,
    exist_ok=True
)

os.makedirs(
    TEMPLATE_DATA_DIR,
    exist_ok=True
)

os.makedirs(
    CHROMA_DIR,
    exist_ok=True
)

os.makedirs(
    FONT_DIR,
    exist_ok=True
)



# ============================================
# STATIC FILES
# ============================================

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

app.mount(
    "/templates",
    StaticFiles(directory=TEMPLATE_DIR),
    name="templates"
)

app.mount(
    "/outputs",
    StaticFiles(directory=OUTPUT_DIR),
    name="outputs"
)

# ============================================
# MODELS
# ============================================

class CampaignRequest(BaseModel):

    campaign: str

# ============================================
# HOME
# ============================================

@app.get("/")
def home():

    return {
        "message":
        "CreativeOS Backend Running"
    }

# ============================================
# PRODUCTS
# ============================================

@app.get("/products")
def get_products():

    products_dir = os.path.join(
        UPLOAD_DIR,
        "products"
    )

    if not os.path.exists(
        products_dir
    ):

        return {
            "products": []
        }

    products = [

        file

        for file in os.listdir(
            products_dir
        )

        if file.endswith(
            (
                ".png",
                ".jpg",
                ".jpeg",
                ".webp"
            )
        )
    ]

    return {
        "products": products
    }

# ============================================
# TEMPLATE LIST
# ============================================

@app.get("/template-list/{ratio}")
def get_templates(

    ratio: str
):

    template_dir = os.path.join(
        TEMPLATE_DIR,
        ratio
    )

    if not os.path.exists(
        template_dir
    ):

        return {
            "templates": []
        }

    templates = []

    for template_name in os.listdir(
        template_dir
    ):

        if template_name.endswith(
            (
                ".png",
                ".jpg",
                ".jpeg",
                ".webp"
            )
        ):

            templates.append({

                "name":
                template_name,

                "image":
                f"/templates/{ratio}/{template_name}"
            })

    return {
        "templates": templates
    }

# ============================================
# UPLOAD PRODUCT
# ============================================

@app.post("/upload-product")
async def upload_product(

    file: UploadFile = File(...)
):

    save_dir = os.path.join(
        UPLOAD_DIR,
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

        "status":
        "success",

        "filename":
        file.filename
    }

# ============================================
# UPLOAD TEMPLATE
# ============================================

@app.post("/upload-template")
async def upload_template(

    ratio: str = Form(...),

    file: UploadFile = File(...)
):

    save_dir = os.path.join(
        TEMPLATE_DIR,
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

    # CREATE TEMPLATE JSON

    json_dir = os.path.join(
        TEMPLATE_DATA_DIR,
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

    template_data = {

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
            template_data,
            f,
            indent=4
        )

    return {

        "status":
        "success",

        "template":
        file.filename
    }

# ============================================
# GENERATE AI CREATIVE
# ============================================

@app.post("/generate-ai-creative")
async def generate_ai_creative(

    campaign: str = Form(...),

    ratio: str = Form(...),

    style: str = Form(...),

    selected_products: str = Form(...),

    template_name: str = Form(...)
):

    try:

        products = json.loads(
            selected_products
        )

        if len(products) == 0:

            return {
                "error":
                "No product selected"
            }

        selected_product = products[0]

        # ====================================
        # PRODUCT PATH
        # ====================================

        product_path = os.path.join(

            UPLOAD_DIR,
            "products",
            selected_product
        )

        # ====================================
        # TEMPLATE JSON
        # ====================================

        template_json_path = os.path.join(

            TEMPLATE_DATA_DIR,

            ratio,

            f"{os.path.splitext(template_name)[0]}.json"
        )

        with open(
            template_json_path,
            "r"
        ) as f:

            template_data = json.load(f)

        # ====================================
        # CHROMA REFERENCES
        # ====================================

        results = collection.query(

            query_texts=[campaign],

            n_results=3
        )

        references = []

        try:

            references = results[
                "documents"
            ][0]

        except:

            references = []

        # ====================================
        # GEMINI PROMPT
        # ====================================

        prompt = f"""
        Create a cinematic premium wellness advertisement.

        Campaign:
        {campaign}

        Style:
        {style}

        Ratio:
        {ratio}

        Template Intelligence:
        {json.dumps(template_data)}

        Previous Creative Learnings:
        {references}

        Rules:

        - Place the product naturally on the platform
        - Maintain cinematic luxury lighting
        - Product should feel realistic
        - Premium wellness aesthetic
        - Scientific modern branding
        - High-end commercial look
        - Beautiful typography
        - Strong composition
        - Ad should feel award-winning
        """

        # ====================================
        # GENERATE IMAGE
        # ====================================

        generated_image = generate_gemini_creative(

            prompt=prompt,

            product_image_path=product_path
        )

        # ====================================
        # SAVE MEMORY
        # ====================================

        collection.add(

            documents=[prompt],

            ids=[str(uuid.uuid4())]
        )

        image_path = (

            generated_image

            if generated_image

            else
            f"/templates/{ratio}/{template_name}"
        )

        return {

            "status":
            "success",

            "generated_image":
            image_path,

            "prompt":
            prompt
        }

    except Exception as e:

        return {

            "status":
            "error",

            "message":
            str(e)
        }

# ============================================
# TEST GEMINI
# ============================================

@app.get("/test-gemini")
def test_gemini():

    response = model.generate_content(
        "Say CreativeOS is working"
    )

    return {
        "response":
        response.text
    }

# ============================================
# RETRIEVE MEMORY
# ============================================

@app.get("/retrieve")
def retrieve(

    query: str
):

    results = collection.query(

        query_texts=[query],

        n_results=5
    )

    return results

# ============================================
# GENERATED IMAGE
# ============================================

@app.get("/generated-image")
def get_generated_image():

    return FileResponse(

        os.path.join(

            OUTPUT_DIR,

            "square_cinematic_generated_ad.png"
        )
    )