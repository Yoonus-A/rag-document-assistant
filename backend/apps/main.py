from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn 

app = FastAPI()



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



if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000)