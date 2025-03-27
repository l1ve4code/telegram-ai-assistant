import os
import asyncio
import re
import requests
from telethon.sync import TelegramClient
from telethon import events
from typing import List, Dict, Optional

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
AI_API_KEY = os.getenv("AI_API_KEY")
FAVORITE_CHAT = "me"
MAX_HISTORY = 10

class DialogManager:
    def __init__(self, max_history: int = MAX_HISTORY):
        self.history: List[Dict] = []
        self.max_history = max_history

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context(self) -> List[Dict]:
        return [
            {"role": "system", "content": "Ты дружелюбный ассистент. Поддерживай диалог."},
            *self.history
        ]

    def clear(self):
        self.history = []


class AIAssistant:
    def __init__(self):
        self.client = TelegramClient('session_file', API_ID, API_HASH)
        self.ai = AIClient(AI_API_KEY)
        self.dialog = DialogManager()
        self.is_active = True
        self.target_user = None
        self.commands = {
            r'\/stop': self.stop_bot,
            r'\/start': self.start_bot,
            r'\/set_user (.+)': self.change_user,
            r'\/clear': self.clear_history
        }

    async def run(self):
        await self.client.start()
        print("Bot started")

        @self.client.on(events.NewMessage(chats=FAVORITE_CHAT))
        async def command_handler(event):
            await self.handle_command(event)

        @self.client.on(events.NewMessage())
        async def message_handler(event):
            if self.is_active and self.target_user and event.sender_id == self.target_user.id:
                await self.handle_message(event)

        await self.client.run_until_disconnected()

    async def handle_command(self, event):
        text = event.text.strip()
        if text.startswith("/"):
            for pattern, action in self.commands.items():
                if match := re.match(pattern, text, re.IGNORECASE):
                    reply_msg = await action(event, *match.groups())

                    await asyncio.sleep(1)
                    await event.delete()

                    await asyncio.sleep(10)
                    await reply_msg.delete()

                    return

            reply_msg = await event.reply("assistant: ❌ Неизвестная команда. Доступные команды:\n"
                                          "/stop - остановить бота\n"
                                          "/start - запустить бота\n"
                                          "/set_user @username - изменить пользователя\n"
                                          "/clear - очистить историю")
            await asyncio.sleep(1)
            await event.delete()
            await asyncio.sleep(10)
            await reply_msg.delete()

    async def stop_bot(self, event, *_):
        self.is_active = False
        return await event.reply("assistant: 🛑 Бот остановлен. Отправьте /start чтобы возобновить.")

    async def start_bot(self, event, *_):
        self.is_active = True
        status = f"с {self.target_user.first_name}" if self.target_user else "без активного диалога"
        return await event.reply(f"assistant: ✅ Бот запущен ({status}). Отправьте /stop чтобы остановить.")

    async def change_user(self, event, username):
        try:
            new_user = await self.client.get_entity(username)
            self.target_user = new_user
            self.dialog.clear()
            return await event.reply(f"assistant: 🔄 Теперь общаюсь с {new_user.first_name}")
        except Exception as e:
            return await event.reply(f"assistant: ❌ Ошибка: {str(e)}")

    async def clear_history(self, event, *_):
        self.dialog.clear()
        return await event.reply("assistant: 🗑️ История диалога очищена")

    async def handle_message(self, event):
        print(f"Message from {self.target_user.first_name}: {event.text}")

        try:
            response = await self.ai.get_response(self.dialog, event.text)
            if not response:
                raise ValueError("Empty AI response")

            async with self.client.action(self.target_user, 'typing'):
                await asyncio.sleep(max(1, min(3, len(response) // 20)))
                await event.reply(response)
        except Exception as e:
            print(f"Error: {str(e)}")
            await event.reply("assistant: ⚠️ Произошла ошибка, попробуйте позже")


class AIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.timeout = 15

    async def get_response(self, dialog: DialogManager, message: str) -> Optional[str]:
        dialog.add_message("user", message)

        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": dialog.get_context(),
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            ai_response = response.json()["choices"][0]["message"]["content"].strip()
            dialog.add_message("assistant", ai_response)
            return ai_response
        except Exception as e:
            print(f"AI Error: {str(e)}")
            return None


if __name__ == "__main__":
    bot = AIAssistant()
    try:
        bot.client.loop.run_until_complete(bot.run())
    except KeyboardInterrupt:
        print("\nBot stopped")
    except Exception as e:
        print(f"Critical error: {str(e)}")