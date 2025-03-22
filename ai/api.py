import requests

from config import API_KEY


def api(text: str) -> str:
    prompt = f"""
    Переведи с молодёжно сленга фразу (именно с молодёжного): {text}.
    Ответь сразу переводом слова без вступлений и постороннего. Максимальная длина 45.
    Если такого слова не существует, то выведи: Такого слова нет.
    """
    # задаем модель и промпт
    data = {
        "stream": False,
        "is_sync": True,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    url_endpoint = "https://api.gen-api.ru/api/v1/networks/claude"
    response = requests.post(url_endpoint, json=data, headers=headers).json()
    return response.get("response")[0]["choices"][0]["message"]["content"]
