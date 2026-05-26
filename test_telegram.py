import requests

BOT_TOKEN = "8676130955:AAFSyovxX_UNT-_EfQnDqQ_xzncjnJQ9KQQ"
CHAT_ID = "7410742810"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "Bot test successful 🚀"
}

response = requests.post(url, json=payload)

print(response.json())