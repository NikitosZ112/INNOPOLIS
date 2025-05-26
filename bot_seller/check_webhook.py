import requests

TOKEN = "7565470355:AAHSYGWszzle69gcdOEbd1ps1NqUPOk60Eg"

# Проверка текущего вебхука
response = requests.get(f"https://api.telegram.org/bot {TOKEN}/getWebhookInfo")
print(response.json())