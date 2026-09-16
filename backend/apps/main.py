from xml.parsers.expat import model

from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn 
import shutil

from service.parser import extract_text_from_pdf
from service.chunker import chunk_pages
from service.vector_store import vectorStore

app = FastAPI()

store = vectorStore()

# create new dir for uploaded files if it doesn't exist
uploads_dir = Path(__file__).parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

class QuestionRequest(BaseModel):
    question: str

@app.post("/process_question")
def handle_question(request: QuestionRequest):
    # feed question to LLM not now

    return {"message": "Question processed."}

@app.post("/file_upload")
async def handle_file_upload(file: UploadFile = File(...)):
    if file is None:
        return {"error": "No file uploaded."}

    save_path = uploads_dir / file.filename
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Process the uploaded file (e.g., extract text, chunk pages, etc.)
    text = extract_text_from_pdf(save_path)
    chunks = chunk_pages(text, chunk_size=1000, overlap=200)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()

    
    store.add_documents(chunks)

    file_size = len(file)
    return {"message": f"File uploaded successfully. Size: {file_size} bytes."}



if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000)

# run uvicorn main:app --reload