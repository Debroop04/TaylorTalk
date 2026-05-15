from fastapi import FastAPI
from pydantic import BaseModel

from agent import get_drive_query
from drive_tool import search_drive

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "TailorTalk backend running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message

    query = get_drive_query(user_message)

    files = search_drive(query)

    if not files:
        return {
            "query": query,
            "response": "No files found"
        }

    results = []

    for file in files:

        results.append(
    {
        "name": file["name"],
        "id": file["id"],
        "mimeType": file["mimeType"]
    }
)

    return {
        "query": query,
        "files": results
    }