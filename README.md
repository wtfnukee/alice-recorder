# Alice Voice Recorder

A Yandex Alice skill that records voice messages and sends them to a Telegram chat.

## Features

- Records all voice messages from Alice
- Sends recorded messages to a specified Telegram chat
- Includes timestamps with each message
- Handles errors gracefully

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/alice-recorder.git
cd alice-recorder
```

2. Create a Telegram bot:
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Use the `/newbot` command to create a new bot
   - Save the bot token you receive

3. Get your Telegram chat ID:
   - Start a chat with your bot
   - Send a message to the bot
   - Visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
   - Look for the "chat" object in the response and find the "id" field

4. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and fill in your Telegram bot token and chat ID

5. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Deploy the skill to Yandex Cloud Functions
2. Configure the environment variables in your cloud function settings
3. Start using the skill with Alice!

## Development

- `skill.py` - Main skill code
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment variables
- `.gitignore` - Git ignore patterns

## License

MIT License
