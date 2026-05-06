# AI Q&A App

## Features
- Upload PDF
- Ask questions
- AI answers using OpenAI
- MongoDB storage
- FAISS vector search

## Setup

### Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

### Frontend
cd frontend
npm install
npm start

## Docker
docker-compose up --build

## Env
export OPENAI_API_KEY=your_key