from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Вставь свой ключ сюда
API_KEY = "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" 

@app.post("/generate/")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "https://render.com",
                "X-Title": "BioRhythm",
            },
            json={
                "model": "google/gemini-2.0-flash-lite-preview:free",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=20
        )
        
        # Если пришла ошибка от OpenRouter, мы её перехватим
        if response.status_code != 200:
            return {"choices": [{"message": {"content": f"ОШИБКА API: {response.text}"}}]}
            
        return response.json()
        
    except Exception as e:
        return {"choices": [{"message": {"content": f"КРИТИЧЕСКАЯ ОШИБКА: {str(e)}"}}]}
