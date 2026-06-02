from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client
import g4f

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Client()

@app.post("/generate/")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    try:
        # Используем автоподбор лучшего живого провайдера из g4f
        response = client.chat.completions.create(
            model=g4f.models.default, # Автоматически выбирает самую стабильную модель (обычно gpt-4o-mini)
            messages=[{"role": "user", "content": prompt}]
        )
        
        ai_text = response.choices[0].message.content
        
        # Если ИИ почему-то вернул пустоту, подстрахуем его текстом
        if not ai_text:
            ai_text = "🔄 Запрос прошел, но ответ оказался пустым. Попробуйте отправить еще раз!"
            
        return {
            "choices": [
                {
                    "message": {
                        "content": ai_text
                    }
                }
            ]
        }

    except Exception as e:
        # Если всё упало, выводим понятную ошибку прямо на экран
        return {"choices": [{"message": {"content": f"❌ Ошибка ИИ: {str(e)}"}}]}