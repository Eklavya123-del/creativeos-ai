import os
import json
import uuid
import shutil

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)
from template_processor import (
    process_template
)
from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.responses import (
    FileResponse
)

from fastapi.staticfiles import (
    StaticFiles
)

import chromadb
import google.generativeai as genai

from nano_banana import (
    generate_nano_banana_prompt
)

from auth import router as auth_router


from creative_pipeline import (
    generate_final_creative
)

# ============================================
# LOAD ENV
# ============================================

load_dotenv()

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
# BASE DIR
# ============================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# ============================================
# PATHS
# ============================================

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

# ============================================
# ENSURE DIRECTORIES
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

os.makedirs(
    os.path.join(
        UPLOAD_DIR,
        "products"
    ),
    exist_ok=True
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
app.include_router(auth_router)
# ============================================
# CORS
# ============================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
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
# HOME
# ============================================

@app.get("/")
def home():

    return {

        "message":
        "AdMate AI Backend Running"
    }

# ============================================
# TEST GEMINI
# ============================================

@app.get("/test-gemini")
def test_gemini():

    response = model.generate_content(
        "Say AdMate AI is working"
    )

    return {

        "response":
        response.text
    }

# ============================================
# PRODUCT LIST
# ============================================

@app.get("/products")
def get_products():

    product_dir = os.path.join(
        UPLOAD_DIR,
        "products"
    )

    products = []

    if os.path.exists(
        product_dir
    ):

        products = os.listdir(
            product_dir
        )

    return {

        "products":
        products
    }

# ============================================
# TEMPLATE LIST
# ============================================
@app.post("/upload-template")
async def upload_template(

    file: UploadFile = File(...)
):

    try:

        master_dir = os.path.join(
            TEMPLATE_DIR,
            "master"
        )

        os.makedirs(
            master_dir,
            exist_ok=True
        )

        template_path = os.path.join(
            master_dir,
            file.filename
        )

        with open(
            template_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        process_template(

            template_path=template_path,

            template_name=file.filename,

            template_dir=TEMPLATE_DIR,

            template_data_dir=TEMPLATE_DATA_DIR
        )

        return {

            "status": "success",

            "filename":
            file.filename
        }

    except Exception as e:

        return {

            "status": "error",

            "message":
            str(e)
        }
@app.get("/template-list/{ratio}")
def get_templates(

    ratio: str
):

    template_dir = os.path.join(

        TEMPLATE_DIR,

        ratio
    )

    templates = []

    if os.path.exists(
        template_dir
    ):

        templates = os.listdir(
            template_dir
        )

    return {

        "templates":
        templates
    }

# ============================================
# UPLOAD PRODUCT
# ============================================

@app.post("/upload-product")
async def upload_product(

    file: UploadFile = File(...)
):

    product_dir = os.path.join(

        UPLOAD_DIR,

        "products"
    )

    os.makedirs(
        product_dir,
        exist_ok=True
    )

    file_path = os.path.join(

        product_dir,

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

    # ====================================
    # PARSE PRODUCTS
    # ====================================

        if selected_products.startswith("["):

            products = json.loads(
                selected_products
            )

        else:

            products = [
                selected_products
            ]

        if len(products) == 0:

            return {

                "status":
                "error",

                "message":
                "No product selected"
            }

        selected_product = products[0]

        # ====================================
        # PRODUCT IMAGE PATH
        # ====================================

        product_path = os.path.join(

            UPLOAD_DIR,

            "products",

            selected_product
        )

        # ====================================
        # TEMPLATE IMAGE PATH
        # ====================================

        template_image_path = os.path.join(

            TEMPLATE_DIR,

            ratio,

            template_name
        )

        # ====================================
        # TEMPLATE JSON PATH
        # ====================================

        template_json_path = os.path.join(

            TEMPLATE_DATA_DIR,

            ratio,

            f"{os.path.splitext(template_name)[0]}.json"
        )

        # ====================================
        # LOAD TEMPLATE DATA
        # ====================================

        template_data = {}

        if os.path.exists(
            template_json_path
        ):

            with open(
                template_json_path,
                "r"
            ) as f:

                template_data = json.load(f)

        # ====================================
        # CHROMA MEMORY
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
        # FINAL PROMPT
        # ====================================

        final_prompt = (
            generate_nano_banana_prompt(

                campaign=campaign,

                style=style,

                ratio=ratio,

                template_data=template_data,

                selected_products=products
            )
        )

        # ====================================
        # RATIO MAP
        # ====================================

        ratio_map = {

            "square": "1:1",

            "story": "9:16",

            "feed": "4:5",

            "banner": "16:9"
        }

        # ====================================
        # STABILITY GENERATION
        # ====================================

        generated_image = (
            generate_final_creative(

                product_path=product_path,

                template_image_path=template_image_path,

                template_json_path=template_json_path,

                prompt=final_prompt,

                ratio=ratio_map.get(
                    ratio,
                    "1:1"
                )
            )
        )

        # ====================================
        # SAVE MEMORY
        # ====================================

        collection.add(

            documents=[final_prompt],

            ids=[str(uuid.uuid4())]
        )

        # ====================================
        # FALLBACK
        # ====================================

        if not generated_image:

            generated_image = (
                f"/templates/{ratio}/{template_name}"
            )

        # ====================================
        # RESPONSE
        # ====================================

        return {

            "status":
            "success",

            "generated_image":
            generated_image
        }

    except Exception as e:

        print(
            "GENERATION ERROR:"
        )

        print(str(e))

        return {

            "status":
            "error",

            "message":
            str(e)
        }

# ============================================
# GENERATED IMAGE
# ============================================

@app.get("/generated-image")
def get_generated_image():

    return FileResponse(

        os.path.join(

            OUTPUT_DIR,

            "generated_ai_creative.png"
        )
    )