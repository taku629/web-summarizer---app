def print_available_models():
    try:
        models = genai.list_models()
        print('利用可能なモデル一覧:')
        for m in models:
            print(f"- {m.name}")
    except Exception as e:
        print(f"モデル一覧の取得に失敗しました: {e}")
# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

genai.configure(api_key="AIzaSyA-e309kfoMh4D0RHlf-1KfdUc3JIFOgN4")

class UrlItem(BaseModel):
    url: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def scrape_text_from_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"URLの取得に失敗しました: {e}")

def summarize_text_with_gemini(text: str) -> str:
    try:
        model = genai.GenerativeModel('models/gemini-2.5-pro')
        truncated_text = text[:15000]
        prompt = f"以下の文章を300文字程度で簡潔に要約してください:\n\n{truncated_text}"
        print("[AIプロンプト先頭300文字]:\n" + prompt[:300])
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AIによる要約中にエラーが発生しました: {e}")

@app.post("/summaries")
def create_summary_endpoint(item: UrlItem):
    print("\n==============================")
    print("[要約リクエスト受信]")
    print(f"\033[93mURL: {item.url}\033[0m")  # 明るい黄色で表示
    print_available_models()  # 利用可能なモデル一覧をリクエストごとに表示
    try:
        scraped_text = scrape_text_from_url(item.url)
        print("[抽出テキスト先頭300文字]:\n" + scraped_text[:300])
        if not scraped_text:
            raise HTTPException(status_code=400, detail="Webサイトからテキストを抽出できませんでした。")
        summary_text = summarize_text_with_gemini(scraped_text)
        print(f"URL ({item.url}) の要約が完了しました。")
        print("==============================\n")
        return {"summary": summary_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print_available_models()