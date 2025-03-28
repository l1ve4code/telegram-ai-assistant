# telegram-ai-assistant

## About

- **Purpose**: Personal AI-powered assistant for one-on-one Telegram conversations with context awareness
- **Key Features**:
  - Real-time conversation with a specific Telegram user
  - Context-aware responses using conversation history
  - Integration with Rimunace AI API for intelligent replies
  - Typing indicators for natural interaction
  - Conversation history management with `/clear` command
  - Automatic reconnection and error handling

### Technologies

* Language: **Python 3.9+**
* Libraries: **Telethon, requests, asyncio**
* APIs: **Telegram API, Rimunace AI API**
* Deployment: **Docker (optional)**

## Installing

### Clone the Project

```shell
git clone https://github.com/l1ve4code/telegram-ai-assistant.git
```

### Replace Placeholders in `docker-compose.yml`

```yaml
services:
  telegram-ai-bot:
    build: .
    container_name: telegram-ai-bot
    environment:
      - API_ID=YOUR_API_ID
      - API_HASH=YOUR_API_HASH
      - AI_API_KEY=YOUR_AI_API_KEY
    restart: unless-stopped
```

## Running the Project

### Using Docker Compose

1. Build and start the container:

```shell
docker-compose up --build
```

2. Stop the container:

```shell
docker-compose down
```

### Running Locally

1. Install dependencies:

```shell
pip install -r requirements.txt
```

2. Run the script:

```shell
python main.py
```

## How It Works

### Main commands (send it to **Saved Messages**)

| Command               | Description                     |
|-----------------------|---------------------------------|
| `/start`              | Activate bot                    |
| `/stop`               | Stop bot                        |
| `/set_user @username` | Change the conversation partner |
| `/clear`              | Clear the dialog history        |

### Automatic deletion of messages
- Your commands will delete after **1 second**
- The bot's responses are deleted after **10 seconds**

### Simple communication
1. Activate bot using command `/start`
2. Write to any user (who added the bot to the contacts)
3. The bot will respond based on the context of the conversation

### Work features
- Communication context saves **last 10 messages**
- The context is reset after restarting the bot

## Author

* Telegram: **[@live4code](https://t.me/live4code)**
* Email: **steven.marelly@gmail.com**

Good luck with your Telegram Chat AI Assistant! 🚀