from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_API_KEY = "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"

@app.post("/generate/")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free", 
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=10
        )
        
        res_json = response.json()
        
        if "error" in res_json:
            error_msg = res_json["error"].get("message", "Ошибка лимитов")
            return {"choices": [{"message": {"content": f"❌ Ошибка скорости: {error_msg}"}}]}
            
        return res_json

    except requests.exceptions.RequestException as e:
        return {"choices": [{"message": {"content": f"❌ Ошибка сети: {str(e)}"}}]}
