from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv
from prompt import COT_TEMPLATE

load_dotenv()

app = FastAPI()

# Serve static HTML
app.mount("/frontend", StaticFiles(directory=r"D:\Tài liệu\2024.2\Sotatek\real_estate_chatbot\frontend"), name="frontend")

# Route "/" trả về file index.html
@app.get("/")
def serve_frontend():
    return FileResponse(r"D:\Tài liệu\2024.2\Sotatek\real_estate_chatbot\frontend\index.html")

@app.get("/favicon.ico")
def favicon():
    # Nếu bạn có file favicon.ico thật, hãy trả về đường dẫn thật
    favicon_path = r"D:\Tài liệu\2024.2\Sotatek\real_estate_chatbot\frontend\favicon.ico"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    # Nếu không có, trả về response rỗng
    return Response(status_code=204)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

class Query(BaseModel):
    user_question: str

def search_web(query: str) -> str:
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    results = data.get("organic_results", [])
    # Gộp snippet và link nguồn
    snippets = []
    for r in results:
        snippet = r.get("snippet", "")
        link = r.get("link", "")
        if snippet and link:
            snippets.append(f"- {snippet} (Nguồn: {link})")
        elif snippet:
            snippets.append(f"- {snippet}")
    return "\n".join(snippets)

@app.post("/ask")
async def ask_real_estate_bot(query: Query):
    search_results = search_web(query.user_question)
    prompt = COT_TEMPLATE.format(
        user_question=query.user_question,
        search_results=search_results
    )

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {"response": completion.choices[0].message.content}
