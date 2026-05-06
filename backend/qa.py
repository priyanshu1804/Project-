from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from db import files_collection
from utils import extract_pdf
from datetime import datetime
from bson import ObjectId

import whisper
import os

DB_PATH = "vector_store"

# load whisper model once
model = whisper.load_model("base")


# 🎧 Transcription
def transcribe(path):
    try:
        result = model.transcribe(path)
        return result["text"], result["segments"]
    except Exception as e:
        print("❌ Transcription error:", e)
        return "Transcription failed", []


# 📂 Process file
def process_file(path):
    text = ""
    segments = None

    # 📄 PDF
    if path.endswith(".pdf"):
        text = extract_pdf(path)

    # 🎥 AUDIO / VIDEO
    elif path.endswith((".mp3", ".wav", ".mp4")):
        text, segments = transcribe(path)

    # 📄 TEXT
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    # 🗄️ Store in MongoDB
    doc = {
        "filename": path,
        "text": text,
        "segments": segments,
        "uploaded_at": datetime.now()
    }

    result = files_collection.insert_one(doc)
    file_id = str(result.inserted_id)

    # ✂️ Split into chunks
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    embeddings = OpenAIEmbeddings()

    # 📦 Create / update FAISS
    if os.path.exists(DB_PATH):
        db = FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        db.add_texts(chunks, metadatas=[{"file_id": file_id}] * len(chunks))
    else:
        db = FAISS.from_texts(
            chunks,
            embeddings,
            metadatas=[{"file_id": file_id}] * len(chunks)
        )

    db.save_local(DB_PATH)


# 🤖 Ask Query
def ask_query(query):
    embeddings = OpenAIEmbeddings()

    # ❌ No DB yet
    if not os.path.exists(DB_PATH):
        return {
            "answer": "❌ Please upload a file first",
            "timestamps": []
        }

    try:
        db = FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        docs = db.similarity_search(query, k=3)

        if not docs:
            return {
                "answer": "❌ No relevant data found",
                "timestamps": []
            }

        answer = " ".join([doc.page_content for doc in docs])

        # ⏱ timestamps (for audio/video)
        timestamps = []

        for doc in docs:
            file_id = doc.metadata.get("file_id")

            if not file_id:
                continue

            file_data = files_collection.find_one(
                {"_id": ObjectId(file_id)}
            )

            if file_data and file_data.get("segments"):
                for seg in file_data["segments"]:
                    if query.lower() in seg["text"].lower():
                        timestamps.append({
                            "start": seg["start"],
                            "end": seg["end"]
                        })

        return {
            "answer": answer,
            "timestamps": timestamps
        }

    except Exception as e:
        return {
            "answer": f"❌ Error: {str(e)}",
            "timestamps": []
        }