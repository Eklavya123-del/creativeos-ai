import chromadb
import uuid


client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = client.get_or_create_collection(
    name="creative_memory"
)


def save_generation(

    campaign,

    style,

    ratio,

    template,

    product,

    final_prompt
):

    collection.add(

        documents=[
            final_prompt
        ],

        metadatas=[{

            "campaign": campaign,

            "style": style,

            "ratio": ratio,

            "template": template,

            "product": product
        }],

        ids=[
            str(uuid.uuid4())
        ]
    )


def retrieve_similar_creatives(

    campaign
):

    results = collection.query(

        query_texts=[
            campaign
        ],

        n_results=3
    )

    return results