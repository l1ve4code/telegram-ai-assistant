import os
import asyncio
import requests
from telethon.sync import TelegramClient
from telethon import events
from typing import List, Dict, Optional

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
AI_API_KEY = os.getenv("AI_API_KEY")
TARGET_USER = os.getenv("TARGET_USER")
MAX_HISTORY = 10

class Conversation:
    def __init__(self, max_history: int = MAX_HISTORY):
        self.history: List[Dict] = []
        self.max_history = max_history

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context(self) -> List[Dict]:
        return [{"role": "system", "content": "Ты дружелюбный ассистент. Поддерживай диалог."}] + self.history

    def clear(self):
        self.history = []

class AIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.rimunace.xyz/v1/chat/completions"
        self.timeout = 15

    async def get_response(self, conversation: Conversation, prompt: str) -> Optional[str]:
        conversation.add_message("user", prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": conversation.get_context(),
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            ai_response = response.json()["choices"][0]["message"]["content"].strip()
            conversation.add_message("assistant", ai_response)
            return ai_response
        except Exception as e:
            print(f"[AI Error] {str(e)}")
            return None

ai = AIClient(AI_API_KEY)
client = TelegramClient('session_file', API_ID, API_HASH)
conversation = Conversation()

async def main():
    try:
        await client.start()

        try:
            target = await client.get_entity(TARGET_USER)
            print(f"Бот запущен. Ожидаю сообщения от {target.first_name}")
        except Exception as e:
            print(f"[Error] User not found: {str(e)}")
            return

        @client.on(events.NewMessage(from_users=target))
        async def handler(event):
            print(f"Получено: {event.text}")

            if event.text.lower() == '/clear':
                conversation.clear()
                await event.reply("История диалога очищена!")
                return

            try:
                response = await ai.get_response(conversation, event.text)

                if not response:
                    raise ValueError("Empty AI response")

                async with client.action(target, 'typing'):
                    delay = max(1, min(5, int(len(response) / 20)))
                    await asyncio.sleep(delay)
                    await event.reply(response)

            except Exception as e:
                print(f"[Handler Error] {str(e)}")
                await event.reply("⚠️ Ошибка, попробуйте позже")

        print("Бот готов (с историей диалога)...")
        await client.run_until_disconnected()

    except Exception as e:
        print(f"[Main Error] {str(e)}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nБот остановлен")
    except Exception as e:
        print(f"[Startup Error] {str(e)}")