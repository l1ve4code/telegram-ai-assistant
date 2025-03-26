import os
import asyncio
import requests
from telethon.sync import TelegramClient
from telethon import events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
AI_API_KEY = os.getenv("AI_API_KEY")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
TARGET_USER = os.getenv("TARGET_USER")

class AIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.rimunace.xyz/v1/chat/completions"

    def get_response(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Ты дружелюбный Telegram-ассистент. Отвечай кратко."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[AI Error] {str(e)}")
            return "Произошла ошибка при обработке запроса."

ai = AIClient(AI_API_KEY)
client = TelegramClient('session_file', API_ID, API_HASH)

async def main():

    await client.start()

    try:
        target = await client.get_entity(TARGET_USER)
        print(f"Бот запущен. Ожидаю сообщения от {target.first_name}")
    except Exception as e:
        print(f"[Error] Не удалось найти пользователя: {str(e)}")
        return

    @client.on(events.NewMessage(from_users=target))
    async def handler(event):
        print(f"Получено сообщение: {event.text}")

        try:
            response = ai.get_response(event.text)

            async with client.action(target, 'typing'):
                await asyncio.sleep(max(1, int(len(response)/20)))
                await event.reply(response)
        except Exception as e:
            print(f"[Error] Ошибка при обработке: {str(e)}")
            await event.reply("⚠️ Произошла ошибка, попробуйте позже.")

    print("Бот готов к работе...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())