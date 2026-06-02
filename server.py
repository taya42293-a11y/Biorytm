from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# СЮДА ВСТАВЬ НОВЫЙ КЛЮЧ
API_KEY = "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" 

@app.post("/generate/")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()
