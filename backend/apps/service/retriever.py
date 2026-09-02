from sentence_transformers import SentenceTransformer
from .vector_store import vectorStore

from google import genai
from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()


# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Vector store
store = vectorStore()


# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def retrieve(query, top_k=3):

    query_embedding = model.encode(query).tolist()

    return store.query(query_embedding, top_k=top_k)


def build_prompt(query, retrieved_chunks):

    context = "\n\n".join(
        f"[Page {c['page_number']}]: {c['text']}"
        for c in retrieved_chunks
    )

    return f"""You are a football rules assistant.

Answer the question using ONLY the context provided below.

If the answer is not contained in the context, say:
"I don't know based on the provided context."

Do not make up or assume information.

Context:

{context}

Question: {query}

Answer:"""


def generate_answer(query, top_k=5):

    # Retrieve relevant chunks
    chunks = retrieve(query, top_k=top_k)

    # Build prompt using retrieved chunks
    prompt = build_prompt(query, chunks)

    # Generate answer using Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return {
        "answer": response.text,
        "sources": [
            {
                "page": c["page_number"],
                "distance": c["distance"]
            }
            for c in chunks
        ]
    }