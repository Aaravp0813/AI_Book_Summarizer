# import os
# import sys
# import io
# import time
# import zipfile
# import logging
# from pathlib import Path
# from pypdf import PdfReader
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from google import genai
# from google.genai import types

# logging.getLogger("pypdf").setLevel(logging.ERROR)

# load_dotenv()

# if not os.getenv("GOOGLE_API_KEY"):
#     raise ValueError("❌ Error: GOOGLE_API_KEY not found in your .env file.")

# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# # --------------------------------------------------
# # SUBJECT CONFIGURATION
# # --------------------------------------------------

# SUBJECTS = {
#     'science': {
#         'label': 'Science',
#         'description': 'NCERT Grade 8 Science'
#     },
#     'maths': {
#         'label': 'Mathematics',
#         'description': 'NCERT Grade 8 Mathematics'
#     },
#     'social_science': {
#         'label': 'Social Science',
#         'description': 'NCERT Grade 8 Social Science'
#     },
#     'english': {
#         'label': 'English',
#         'description': 'NCERT Grade 8 English'
#     },
# }


# # --------------------------------------------------
# # CHUNKING CONFIGURATION (Same for all subjects)
# # --------------------------------------------------

# CHUNK_SIZE = 1800
# OVERLAP = 250
# BATCH_SIZE = 20
# EMBEDDING_MODEL = "models/gemini-embedding-001"


# # --------------------------------------------------
# # TEXT EXTRACTION & CHUNKING
# # --------------------------------------------------

# def extract_and_chunk_zip(zip_path, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
#     """
#     Extract and chunk text from a ZIP file containing PDFs.
#     Uses the same methodology as the existing Science implementation.
    
#     Args:
#         zip_path: Path to ZIP file containing PDFs
#         chunk_size: Size of each chunk (default: 1800)
#         overlap: Overlap between chunks (default: 250)
        
#     Returns:
#         List of text chunks with source metadata
#     """
#     full_text = []
    
#     with zipfile.ZipFile(zip_path, 'r') as archive:
#         for file_name in archive.namelist():
#             if file_name.endswith('.pdf') and not file_name.startswith('__MACOSX'):
                
#                 with archive.open(file_name) as pdf_file:
#                     pdf_stream = io.BytesIO(pdf_file.read())
#                     reader = PdfReader(pdf_stream)
                    
#                     for i, page in enumerate(reader.pages):
#                         page_text = page.extract_text(
#                             extraction_mode="layout", 
#                             layout_mode_strip_rotated=False
#                         )
#                         if page_text.strip():
#                             full_text.append(f"\n[Source: {file_name} | Page {i+1}]\n{page_text}")
                            
#     text = "\n".join(full_text)
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + chunk_size
#         chunks.append(text[start:end])
#         start += (chunk_size - overlap)
        
#     return chunks


# # --------------------------------------------------
# # FAISS INDEX BUILDING
# # --------------------------------------------------

# def build_langchain_faiss(chunks, subject_label):
#     """
#     Build a FAISS index from text chunks using Gemini embeddings.
#     Uses the same methodology as the existing Science implementation.
    
#     Args:
#         chunks: List of text chunks
#         subject_label: Label for the subject (for logging)
        
#     Returns:
#         FAISS vector store object
#     """
#     embeddings_model = GoogleGenerativeAIEmbeddings(
#         model=EMBEDDING_MODEL
#     )

#     total_chunks = len(chunks)
#     total_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE

#     db = None

#     print(f"\n📚 {subject_label}: Total chunks: {total_chunks}")
#     print(f"📦 Batch size: {BATCH_SIZE}")
#     print(f"🚀 Total embedding batches: {total_batches}")

#     for batch_num in range(total_batches):

#         start_idx = batch_num * BATCH_SIZE
#         end_idx = min(
#             start_idx + BATCH_SIZE,
#             total_chunks
#         )

#         batch = chunks[start_idx:end_idx]

#         print(
#             f"\r⏳ {subject_label}: Processing batch "
#             f"{batch_num+1}/{total_batches} "
#             f"({end_idx}/{total_chunks} chunks)",
#             end=""
#         )

#         retry_count = 0

#         while retry_count < 5:

#             try:

#                 if db is None:
#                     db = FAISS.from_texts(
#                         texts=batch,
#                         embedding=embeddings_model
#                     )
#                 else:
#                     db.add_texts(batch)

#                 break

#             except Exception as e:

#                 error_text = str(e)

#                 if (
#                     "429" in error_text
#                     or "RESOURCE_EXHAUSTED" in error_text
#                 ):

#                     retry_count += 1

#                     wait_time = min(
#                         60 * retry_count,
#                         300
#                     )

#                     print(
#                         f"\n⏸️ {subject_label}: Rate limit hit. "
#                         f"Waiting {wait_time}s..."
#                     )

#                     time.sleep(wait_time)

#                 else:
#                     raise

#         time.sleep(2.0)

#     print(
#         f"\n✅ {subject_label}: Finished indexing "
#         f"{total_chunks} chunks."
#     )

#     if db is None:
#         raise RuntimeError(f"❌ FAISS database was not created for {subject_label}.")

#     return db


# # --------------------------------------------------
# # SUBJECT-SPECIFIC INDEX BUILDER
# # --------------------------------------------------

# def build_subject_index(subject_id, zip_path, output_dir):
#     """
#     Build and save a FAISS index for a specific subject.
#     This is the main function to call when indexing a new subject.
    
#     Args:
#         subject_id: Subject identifier (e.g., 'science', 'maths')
#         zip_path: Path to ZIP file containing subject PDFs
#         output_dir: Directory to save the FAISS index
        
#     Returns:
#         Path to the saved FAISS index
#     """
#     if subject_id not in SUBJECTS:
#         raise ValueError(f"Unknown subject: {subject_id}")
    
#     subject_info = SUBJECTS[subject_id]
#     subject_label = subject_info['label']
    
#     print(f"\n{'='*60}")
#     print(f"Building {subject_label} FAISS Index")
#     print(f"{'='*60}")
    
#     # Create output directory if needed
#     index_output_path = os.path.join(output_dir, subject_id)
#     os.makedirs(index_output_path, exist_ok=True)
    
#     # Extract and chunk
#     print(f"\n📖 Extracting and chunking {zip_path}...")
#     chunks = extract_and_chunk_zip(zip_path)
#     print(f"✅ Created {len(chunks)} chunks")
    
#     # Build FAISS
#     print(f"\n🧠 Building FAISS index for {subject_label}...")
#     vector_store = build_langchain_faiss(chunks, subject_label)
    
#     # Save FAISS
#     print(f"\n💾 Saving FAISS index to {index_output_path}...")
#     vector_store.save_local(index_output_path)
#     print(f"✅ FAISS index saved")
    
#     return index_output_path


# # --------------------------------------------------
# # EXAMPLE USAGE & TESTING
# # --------------------------------------------------

# if __name__ == "__main__":
#     """
#     IMPORTANT: This script is for building subject-specific FAISS indexes.
    
#     The Science database has already been built and is working.
    
#     To build indexes for other subjects, you would use:
    
#     build_subject_index(
#         subject_id='maths',
#         zip_path='/path/to/maths_textbook.zip',
#         output_dir='./faiss_ncert_db'
#     )
    
#     But DO NOT run this script during the multi-subject implementation phase.
#     The script is ready; the execution will happen manually later.
#     """
    
#     print("✅ Multi-subject FAISS indexing pipeline is ready.")
#     print("\nSupported subjects:")
#     for subject_id, info in SUBJECTS.items():
#         print(f"  - {subject_id}: {info['label']}")
    
#     print("\nConfiguration:")
#     print(f"  Chunk size: {CHUNK_SIZE} chars")
#     print(f"  Overlap: {OVERLAP} chars")
#     print(f"  Batch size: {BATCH_SIZE} chunks")
#     print(f"  Embedding model: {EMBEDDING_MODEL}")

#     full_text = []
    
#     with zipfile.ZipFile(zip_path, 'r') as archive:
#         for file_name in archive.namelist():
#             if file_name.endswith('.pdf') and not file_name.startswith('__MACOSX'):
                
#                 with archive.open(file_name) as pdf_file:
#                     pdf_stream = io.BytesIO(pdf_file.read())
#                     reader = PdfReader(pdf_stream)
                    
#                     for i, page in enumerate(reader.pages):
#                         page_text = page.extract_text(
#                             extraction_mode="layout", 
#                             layout_mode_strip_rotated=False
#                         )
#                         if page_text.strip():
#                             full_text.append(f"\n[Source: {file_name} | Page {i+1}]\n{page_text}")
                            
#     text = "\n".join(full_text)
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + chunk_size
#         chunks.append(text[start:end])
#         start += (chunk_size - overlap)
        
#     return chunks

# def build_langchain_faiss(chunks):
#     model_string = "models/gemini-embedding-001"
#     embeddings_model = GoogleGenerativeAIEmbeddings(
#         model=model_string
#     )

#     BATCH_SIZE = 20

#     total_chunks = len(chunks)
#     total_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE

#     db = None

#     print(f"\n📚 Total chunks: {total_chunks}")
#     print(f"📦 Batch size: {BATCH_SIZE}")
#     print(f"🚀 Total embedding batches: {total_batches}")

#     for batch_num in range(total_batches):

#         start_idx = batch_num * BATCH_SIZE
#         end_idx = min(
#             start_idx + BATCH_SIZE,
#             total_chunks
#         )

#         batch = chunks[start_idx:end_idx]

#         print(
#             f"\r⏳ Processing batch "
#             f"{batch_num+1}/{total_batches} "
#             f"({end_idx}/{total_chunks} chunks)",
#             end=""
#         )

#         retry_count = 0

#         while retry_count < 5:

#             try:

#                 if db is None:
#                     db = FAISS.from_texts(
#                         texts=batch,
#                         embedding=embeddings_model
#                     )
#                 else:
#                     db.add_texts(batch)

#                 break

#             except Exception as e:

#                 error_text = str(e)

#                 if (
#                     "429" in error_text
#                     or "RESOURCE_EXHAUSTED" in error_text
#                 ):

#                     retry_count += 1

#                     wait_time = min(
#                         60 * retry_count,
#                         300
#                     )

#                     print(
#                         f"\n⏸️ Rate limit hit."
#                         f" Waiting {wait_time}s..."
#                     )

#                     time.sleep(wait_time)

#                 else:
#                     raise

#         time.sleep(2.0)

#     print(
#         f"\n✅ Finished indexing "
#         f"{total_chunks} chunks."
#     )

#     if db is None:
#         raise RuntimeError("❌ FAISS database was not created.")

#     return db


# def ask_gemini_rag(query, vector_store, k=5):
#     matches = vector_store.similarity_search(query,k=5)
#     context_blocks = [doc.page_content for doc in matches]
#     context = "\n---\n".join(context_blocks)
    
#     system_instruction = (
#     "You are an expert AI tutor helping a student study from NCERT textbooks. "
#     "Answer strictly using the provided textbook context. "
#     "Be concise by default. Provide detailed explanations only when the student explicitly requests it. "
#     "If the context does not contain the answer, politely say you cannot find it in these documents."
# )
#     user_prompt = f"Context from textbooks:\n{context}\n\nQuestion: {query}"
    
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=user_prompt,
#         config=types.GenerateContentConfig(
#             system_instruction=system_instruction,
#             temperature=0.3
#         )
#     )
#     print(f"\n📚 AI Tutor Answer:\n{response.text}")

# def interactive_tutor_session(zip_path):
#     index_folder = r"E:\My_Projects\faiss_ncert_db"
#     model_string = "gemini-embedding-001"
#     embeddings_model = GoogleGenerativeAIEmbeddings(model=model_string)
    
#     if os.path.exists(index_folder):
#         print("📁 Existing FAISS index found on your E: drive. Loading instantly...")
#         vector_store = FAISS.load_local(index_folder, embeddings_model, allow_dangerous_deserialization=True)
#     else:
#         print("📦 Processing your 54MB archive for the first time. Please wait...")
#         try:
#             chunks = extract_and_chunk_zip(zip_path)
#             vector_store = build_langchain_faiss(chunks)
#             vector_store.save_local(index_folder)
#             print(f"💾 Saved index to disk at '{index_folder}' for subsequent zero-wait loads.")
#         except Exception as e:
#             print(f"❌ Setup error occurred: {e}")
#             return
    
#     print("\n🚀 Ready! Type 'exit' or 'quit' to close.")
#     print("-----------------------------------------")
    
#     while True:
#         try:
#             query = input("\n🧑‍🎓 Ask a question: ")
#             if query.strip().lower() in ['exit', 'quit']:
#                 print("👋 Session finished.")
#                 break
#             if not query.strip():
#                 continue
                
#             ask_gemini_rag(query, vector_store)
#         except KeyboardInterrupt:
#             print("\n👋 Session closed.")
#             sys.exit(0)

# if __name__ == "__main__":
#     target_folder = r"E:\My_Projects"
#     target_zip = None
#     script_directory = Path(__file__).resolve().parent
    
#     if os.path.exists(target_folder):
#         for file in os.listdir(target_folder):
#             if "NCERT" in file.upper() and file.lower().endswith(".zip"):
#                 target_zip = os.path.join(target_folder, file)
#                 break
                
#     if not target_zip and os.path.exists(script_directory):
#         for file in os.listdir(script_directory):
#             if "NCERT" in file.upper() and file.lower().endswith(".zip"):
#                 target_zip = os.path.join(script_directory, file)
#                 break
                
#     if target_zip:
#         interactive_tutor_session(target_zip)
#     else:
#         print(f"❌ Diagnostic Error: Python could not find any matching NCERT zip archive inside E:\\My_Projects.")


#================================================================================================================================================================

import os
import sys
import io
import time
import zipfile
import logging
from pathlib import Path
from pypdf import PdfReader
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from google import genai
from google.genai import types

logging.getLogger("pypdf").setLevel(logging.ERROR)

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("❌ Error: GOOGLE_API_KEY not found in your .env file.")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# --------------------------------------------------
# SUBJECT CONFIGURATION
# --------------------------------------------------

SUBJECTS = {
    'science': {
        'label': 'Science',
        'description': 'NCERT Grade 8 Science',
        "embedding_model": "models/gemini-embedding-001",
    },
    'maths': {
        'label': 'Mathematics',
        'description': 'NCERT Grade 8 Mathematics',
        "embedding_model": "models/gemini-embedding-2",
    },
    'social_science': {
        'label': 'Social Science',
        'description': 'NCERT Grade 8 Social Science',
        "embedding_model": "models/gemini-embedding-001",
    },
    'english': {
        'label': 'English',
        'description': 'NCERT Grade 8 English',
        "embedding_model": "models/gemini-embedding-001",
    },
}


# --------------------------------------------------
# CHUNKING CONFIGURATION (Same for all subjects)
# --------------------------------------------------

CHUNK_SIZE = 1800
OVERLAP = 250
BATCH_SIZE = 20
EMBEDDING_MODEL = "models/gemini-embedding-001"


# --------------------------------------------------
# TEXT EXTRACTION & CHUNKING
# --------------------------------------------------

def extract_and_chunk_zip(zip_path, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Extract and chunk text from a ZIP file containing PDFs.

    Args:
        zip_path: Path to ZIP file containing PDFs
        chunk_size: Size of each chunk (default: 1800)
        overlap: Overlap between chunks (default: 250)

    Returns:
        List of text chunks with source metadata
    """
    full_text = []

    with zipfile.ZipFile(zip_path, 'r') as archive:
        for file_name in archive.namelist():
            if file_name.endswith('.pdf') and not file_name.startswith('__MACOSX'):

                with archive.open(file_name) as pdf_file:
                    pdf_stream = io.BytesIO(pdf_file.read())
                    reader = PdfReader(pdf_stream)

                    for i, page in enumerate(reader.pages):
                        page_text = page.extract_text(
                            extraction_mode="layout",
                            layout_mode_strip_rotated=False
                        )
                        if page_text.strip():
                            full_text.append(f"\n[Source: {file_name} | Page {i+1}]\n{page_text}")

    text = "\n".join(full_text)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)

    return chunks


# --------------------------------------------------
# FAISS INDEX BUILDING
# --------------------------------------------------

def build_langchain_faiss(chunks, subject_label="Book", embedding_model=EMBEDDING_MODEL):
    """
    Build a FAISS index from text chunks using Gemini embeddings.

    Args:
        chunks: List of text chunks
        subject_label: Label for the subject (for logging). Defaults to
            "Book" so this can also be called from the single-book
            interactive tutor flow without passing a subject.

    Returns:
        FAISS vector store object
    """
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model=embedding_model
    )

    total_chunks = len(chunks)
    total_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE

    db = None

    print(f"\n📚 {subject_label}: Total chunks: {total_chunks}")
    print(f"📦 Batch size: {BATCH_SIZE}")
    print(f"🚀 Total embedding batches: {total_batches}")

    for batch_num in range(total_batches):

        start_idx = batch_num * BATCH_SIZE
        end_idx = min(
            start_idx + BATCH_SIZE,
            total_chunks
        )

        batch = chunks[start_idx:end_idx]

        print(
            f"\r⏳ {subject_label}: Processing batch "
            f"{batch_num+1}/{total_batches} "
            f"({end_idx}/{total_chunks} chunks)",
            end=""
        )

        retry_count = 0

        while retry_count < 5:

            try:

                if db is None:
                    db = FAISS.from_texts(
                        texts=batch,
                        embedding=embeddings_model
                    )
                else:
                    db.add_texts(batch)

                break

            except Exception as e:

                error_text = str(e)

                if (
                    "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                ):

                    retry_count += 1

                    wait_time = min(
                        60 * retry_count,
                        300
                    )

                    print(
                        f"\n⏸️ {subject_label}: Rate limit hit. "
                        f"Waiting {wait_time}s..."
                    )

                    time.sleep(wait_time)

                else:
                    raise

        time.sleep(2.0)

    print(
        f"\n✅ {subject_label}: Finished indexing "
        f"{total_chunks} chunks."
    )

    if db is None:
        raise RuntimeError(f"❌ FAISS database was not created for {subject_label}.")

    return db


# --------------------------------------------------
# SUBJECT-SPECIFIC INDEX BUILDER
# --------------------------------------------------

def build_subject_index(subject_id, zip_path, output_dir):
    """
    Build and save a FAISS index for a specific subject.

    Args:
        subject_id: Subject identifier (e.g., 'science', 'maths')
        zip_path: Path to ZIP file containing subject PDFs
        output_dir: Directory to save the FAISS index

    Returns:
        Path to the saved FAISS index
    """
    if subject_id not in SUBJECTS:
        raise ValueError(f"Unknown subject: {subject_id}")

    subject_info = SUBJECTS[subject_id]
    subject_label = subject_info['label']

    print(f"\n{'='*60}")
    print(f"Building {subject_label} FAISS Index")
    print(f"{'='*60}")

    index_output_path = os.path.join(output_dir, subject_id)
    os.makedirs(index_output_path, exist_ok=True)

    print(f"\n📖 Extracting and chunking {zip_path}...")
    chunks = extract_and_chunk_zip(zip_path)
    print(f"✅ Created {len(chunks)} chunks")

    print(f"\n🧠 Building FAISS index for {subject_label}...")
    
    embedding_model = subject_info["embedding_model"]
    vector_store = build_langchain_faiss(chunks, subject_label, embedding_model)

    print(f"\n💾 Saving FAISS index to {index_output_path}...")
    vector_store.save_local(index_output_path)
    print(f"✅ FAISS index saved")

    return index_output_path


# --------------------------------------------------
# RAG QUERY / INTERACTIVE TUTOR
# --------------------------------------------------

def ask_gemini_rag(query, vector_store, k=5):
    matches = vector_store.similarity_search(query, k=k)
    context_blocks = [doc.page_content for doc in matches]
    context = "\n---\n".join(context_blocks)

    system_instruction = (
        "You are an expert AI tutor helping a student study from NCERT textbooks. "
        "Answer strictly using the provided textbook context. "
        "Be concise by default. Provide detailed explanations only when the student explicitly requests it. "
        "If the context does not contain the answer, politely say you cannot find it in these documents."
    )
    user_prompt = f"Context from textbooks:\n{context}\n\nQuestion: {query}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3
        )
    )
    print(f"\n📚 AI Tutor Answer:\n{response.text}")


def interactive_tutor_session(zip_path):
    index_folder = r"E:\My_Projects\faiss_ncert_db"
    embeddings_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    if os.path.exists(index_folder):
        print("📁 Existing FAISS index found on your E: drive. Loading instantly...")
        vector_store = FAISS.load_local(
            index_folder, embeddings_model, allow_dangerous_deserialization=True
        )
    else:
        print("📦 Processing your archive for the first time. Please wait...")
        try:
            chunks = extract_and_chunk_zip(zip_path)
            vector_store = build_langchain_faiss(chunks, "NCERT")
            vector_store.save_local(index_folder)
            print(f"💾 Saved index to disk at '{index_folder}' for subsequent zero-wait loads.")
        except Exception as e:
            print(f"❌ Setup error occurred: {e}")
            return

    print("\n🚀 Ready! Type 'exit' or 'quit' to close.")
    print("-----------------------------------------")

    while True:
        try:
            query = input("\n🧑‍🎓 Ask a question: ")
            if query.strip().lower() in ['exit', 'quit']:
                print("👋 Session finished.")
                break
            if not query.strip():
                continue

            ask_gemini_rag(query, vector_store)
        except KeyboardInterrupt:
            print("\n👋 Session closed.")
            sys.exit(0)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    """
    Locates an NCERT zip archive under E:\\My_Projects (or next to this
    script) and launches an interactive tutor session against it,
    building/loading a FAISS index as needed.

    To build a dedicated index for a specific subject instead, call:

        build_subject_index(
            subject_id='maths',
            zip_path='/path/to/maths_textbook.zip',
            output_dir='./faiss_ncert_db'
        )
    """

    build_subject_index(
        subject_id='social_science',
        zip_path='E:/My_Projects/NCERT_social_science_textbook.zip',
        output_dir='./faiss_ncert_db')

    target_folder = r"E:\My_Projects"
    target_zip = None
    script_directory = Path(__file__).resolve().parent

    if os.path.exists(target_folder):
        for file in os.listdir(target_folder):
            if "NCERT" in file.upper() and file.lower().endswith(".zip"):
                target_zip = os.path.join(target_folder, file)
                break

    if not target_zip and os.path.exists(script_directory):
        for file in os.listdir(script_directory):
            if "NCERT" in file.upper() and file.lower().endswith(".zip"):
                target_zip = os.path.join(script_directory, file)
                break

    if target_zip:
        print("tutor disabled for now.")
#       interactive_tutor_session(target_zip)
    else:
        print("❌ Diagnostic Error: Python could not find any matching NCERT zip archive inside E:\\My_Projects.")