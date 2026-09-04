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
        "http://localhost:5174",
        "https://ai-book-summarizer-blue.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# SUBJECT CONFIGURATION
# --------------------------------------------------

COMMON_INSTRUCTIONS = (
    "You are an expert AI tutor helping a student study NCERT Grade 8.",
    "Do not use LaTeX formatting, math mode blocks, or LaTeX commands.",
    "Always insert actual raw Unicode symbols directly into the text.",
    "Answer strictly using the provided textbook context.",
    "Be concise by default.",
    "Provide detailed explanations only when explicitly requested.",
    "If the context does not contain the answer, politely say that you cannot find it in these documents."
)

SUBJECTS = {
    'science': {
        'label': 'Science',
        'embedding_model': 'models/gemini-embedding-001',
        'index_folder': r'./faiss_ncert_db/science',
        'system_instruction': (
            "study NCERT Grade 8 Science.",
        )
    },

    'maths': {
        'label': 'Mathematics',
        'embedding_model': 'models/gemini-embedding-2',
        'index_folder': r'./faiss_ncert_db/maths',
        'system_instruction': (
            "study NCERT Grade 8 Mathematics.",
        )
    },

    'social_science': {
        'label': 'Social Science',
        'embedding_model': 'models/gemini-embedding-001',
        'index_folder': r'./faiss_ncert_db/social_science',
        'system_instruction': (
            "study NCERT Grade 8 Social Science.",
        )
    },

    'english': {
        'label': 'English',
        'embedding_model': 'models/gemini-embedding-001',
        'index_folder': r'./faiss_ncert_db/english',
        'system_instruction': (
            "study NCERT Grade 8 English.",
        )
    },
}


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class QuestionRequest(BaseModel):
    subject: str
    question: str


# --------------------------------------------------
# LOAD FAISS DATABASES
# --------------------------------------------------

DB_BASE_PATH = r"./faiss_ncert_db"


vector_stores = {}

for subject_id, config in SUBJECTS.items():

    subject_path = config["index_folder"]
    embedding_model = config["embedding_model"]

    # Science currently exists in the old flat location.
    if (
        subject_id == "science"
        and not os.path.exists(subject_path)
    ):
        subject_path = DB_BASE_PATH

    if not os.path.exists(subject_path):
        print(
            f"⚠️ {config['label']} FAISS database "
            f"not found at {subject_path}"
        )
        continue

    try:
        print(
            f"📁 Loading {config['label']} FAISS database..."
        )

        print(
            f"🧠 Using embedding model: {embedding_model}"
        )

        embeddings_model = GoogleGenerativeAIEmbeddings(
            model=embedding_model
        )

        vector_stores[subject_id] = FAISS.load_local(
            subject_path,
            embeddings_model,
            allow_dangerous_deserialization=True
        )

        print(
            f"✅ {config['label']} FAISS database loaded."
        )

    except Exception as e:
        print(
            f"⚠️ Could not load "
            f"{config['label']} FAISS database: {e}"
        )


# --------------------------------------------------
# ASK ENDPOINT
# --------------------------------------------------

@app.post("/ask")
async def ask_question(request: QuestionRequest):

    subject = request.subject.strip().lower()
    
    # Validate subject
    if subject not in SUBJECTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid subject '{subject}'. Supported subjects: {', '.join(SUBJECTS.keys())}"
        )
    
    # Check if subject database is available
    if subject not in vector_stores or vector_stores[subject] is None:
        subject_label = SUBJECTS[subject]['label']
        raise HTTPException(
            status_code=503,
            detail=f"The {subject_label} NCERT database has not been built yet. Please try a different subject."
        )

    vector_store = vector_stores[subject]
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
        k=20
    )

    context_blocks = [
        doc.page_content
        for doc in matches
    ]

    context = "\n---\n".join(context_blocks)


    # ----------------------------------------------
    # GEMINI
    # ----------------------------------------------

    system_instruction = " ".join(
    COMMON_INSTRUCTIONS +
    SUBJECTS[subject]['system_instruction']
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