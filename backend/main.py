import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
from google import genai
from google.genai import types

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# ENVIRONMENT
# --------------------------------------------------

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env")

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# --------------------------------------------------
# FASTAPI
# --------------------------------------------------

app = FastAPI(
    title="NCERT AI Tutor API"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str


# --------------------------------------------------
# LOAD FAISS
# --------------------------------------------------

INDEX_FOLDER = r"E:\My_Projects\AI_Book_Summarizer\faiss_ncert_db"

EMBEDDING_MODEL = "models/gemini-embedding-001"

embeddings_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL
)

try:

    print("📁 Loading FAISS database...")

    vector_store = FAISS.load_local(
        INDEX_FOLDER,
        embeddings_model,
        allow_dangerous_deserialization=True
    )

    print("✅ FAISS database loaded.")

except Exception as e:

    print(f"❌ Could not load FAISS database: {e}")

    vector_store = None


# --------------------------------------------------
# ASK ENDPOINT
# --------------------------------------------------

@app.post("/ask")
async def ask_question(request: QuestionRequest):

    if vector_store is None:
        raise HTTPException(
            status_code=500,
            detail="FAISS database is not loaded."
        )

    query = request.question.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    # ----------------------------------------------
    # FAISS SEARCH
    # ----------------------------------------------

    matches = vector_store.similarity_search(
        query,
        k=5
    )

    context_blocks = [
        doc.page_content
        for doc in matches
    ]

    context = "\n---\n".join(context_blocks)


    # ----------------------------------------------
    # GEMINI
    # ----------------------------------------------

    system_instruction = (
        "You are an expert AI tutor helping a student "
        "study from NCERT textbooks. "

        "Answer strictly using the provided textbook "
        "context. "

        "Be concise by default. Provide detailed "
        "explanations only when explicitly requested. "

        "If the context does not contain the answer, "
        "politely say that you cannot find it in these "
        "documents."
    )


    user_prompt = f"""
Context from NCERT textbooks:

{context}

Student question:

{query}
"""


    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",

            contents=user_prompt,

            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            )
        )

        answer = response.text


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Gemini API error: {str(e)}"
        )


    # ----------------------------------------------
    # RETURN TO REACT
    # ----------------------------------------------

    return {
        "question": query,
        "answer": answer
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "status": "online",
        "message": "NCERT AI Tutor API is running"
    }