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
    volumes:
      - ./data:/app/data
    environment:
      - API_ID=YOUR_API_ID
      - API_HASH=YOUR_API_HASH
      - AI_API_KEY=YOUR_AI_API_KEY
      - TARGET_USER=YOUR_TARGET_USER
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

1. **Initialization**:
   - Authenticates with Telegram using your API credentials.
   - Establishes connection with the target user specified in `TARGET_USER`.

2. **Message Processing**:
   - Maintains conversation history (last 10 messages by default).
   - Sends conversation context + new message to Rimunace AI API.
   - Returns AI-generated response to the user.

3. **Context Management**:
   - Preserves conversation flow using message history.
   - Clear history anytime with `/clear` command
   - Adjustable history depth via `MAX_HISTORY` variable

4. **Error Handling**:
   - Automatic reconnection on network issues
   - Graceful error recovery with user notifications
   - Detailed error logging in console

## Author

* Telegram: **[@live4code](https://t.me/live4code)**
* Email: **steven.marelly@gmail.com**

Good luck with your Telegram Chat AI Assistant! 🚀