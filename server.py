from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

API_KEY = "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" # Вставь свой ключ сюда

@app.post("/generate/")
async def generate_text(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemini-2.0-flash-lite-preview:free",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        return response.json()
    except Exception as e:
        return {"choices": [{"message": {"content": f"Ошибка: {str(e)}"}}]}
