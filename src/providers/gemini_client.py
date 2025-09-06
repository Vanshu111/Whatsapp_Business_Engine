import requests
def gemini_chat(prompt: str, key: str, max_tokens=120):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {"contents":[{"role":"user","parts":[{"text": prompt}]}],
               "generationConfig":{"maxOutputTokens": max_tokens, "temperature":0.7}}
    r = requests.post(url, json=payload, timeout=10); r.raise_for_status()
    return r.json()['candidates'][0]['content']['parts'][0]['text'].strip()
