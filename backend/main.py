from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from qa import process_file, ask_query
from db import files_collection
from langchain_openai import OpenAI

import os

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📂 Upload
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        path = f"temp_{file.filename}"

        with open(path, "wb") as f:
            f.write(await file.read())

        process_file(path)

        return {"msg": "✅ File uploaded successfully"}

    except Exception as e:
        return {"error": str(e)}


# 🤖 Ask
@app.get("/ask")
def ask(question: str):
    return ask_query(question)


# 📝 Summarize
@app.get("/summarize")
def summarize():
    try:
        data = files_collection.find().sort("uploaded_at", -1).limit(1)[0]

        llm = OpenAI()
        summary = llm(f"Summarize this:\n{data['text'][:3000]}")

        return {"summary": summary}

    except Exception as e:
        return {"error": str(e)}