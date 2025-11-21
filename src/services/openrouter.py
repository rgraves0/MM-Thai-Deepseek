import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_translation(text: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # အခမဲ့ + မြန်မာ/ထိုင်း အရမ်းကောင်းတဲ့ model
    model = "google/gemma-2-27b-it:free"   # ဒါမှမဟုတ် "meta-llama/llama-3.1-8b-instruct:free"
    
    prompt = f"""
    You are the world's best Thai ↔ Myanmar dictionary.
    Input: "{text}"
    
    - Auto-detect language
    - Translate to the other language naturally
    - Provide Romanization for Thai (in parentheses)
    - Give short definition
    - Give 1 example sentence if possible
    
    If input is Thai → respond in Myanmar
    If input is Myanmar → respond in Thai
    Be polite and natural.
    """
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 600
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": os.getenv("WEBHOOK_HOST", "https://yourbot.com"),
        "X-Title": "Thai-Myanmar Dictionary"
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ขออภัย ระบบมีปัญหาชั่วคราว: {str(e)}"

def get_explanation(text: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    model = "google/gemma-2-27b-it:free"
    
    prompt = f"""
    ให้คำอธิบายเชิงลึกสำหรับคำหรือวลีนี้: "{text}"
    - ไวยากรณ์
    - การใช้จริงในชีวิตประจำวัน
    - คำที่คล้ายกัน 3-5 คำ
    - ข้อควรระวัง (ถ้ามี)
    ตอบเป็นภาษาพม่าถ้าคำถามเป็นไทย
    ตอบเป็นภาษาไทยถ้าคำถามเป็นพม่า
    """
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 800
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": os.getenv("WEBHOOK_HOST", "https://yourbot.com"),
        "X-Title": "Thai-Myanmar Dictionary"
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=40)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "ไม่สามารถอธิบายเพิ่มเติมได้ในขณะนี้"
