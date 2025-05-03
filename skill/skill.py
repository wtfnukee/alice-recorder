import os
import json
import requests
from datetime import datetime
from requests.exceptions import RequestException

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_to_telegram(message):
    """
    Send message to Telegram channel
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise Exception("Missing Telegram configuration (BOT_TOKEN or CHAT_ID)")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()

        result = response.json()
        if not result.get("ok"):
            raise Exception(
                f"Telegram API error: {result.get('description', 'Unknown error')}"
            )

        return True
    except RequestException as e:
        raise Exception(f"Network error while sending to Telegram: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Invalid response from Telegram API")
    except Exception as e:
        raise Exception(f"Unexpected error while sending to Telegram: {str(e)}")


def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    try:
        text = "Диктофон включен"

        if not isinstance(event, dict):
            raise ValueError("Invalid event format")

        if "request" not in event:
            raise ValueError("Missing 'request' in event")

        if "original_utterance" not in event["request"]:
            return {
                "version": event["version"],
                "session": event["session"],
                "response": {"text": text, "end_session": "false"},
            }

        utterance = event["request"]["original_utterance"].strip()
        if not utterance:
            return {
                "version": event["version"],
                "session": event["session"],
                "response": {
                    "text": "Я вас не расслышала, повторите пожалуйста",
                    "end_session": "false",
                },
            }

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"<b>Новое сообщение ({timestamp}):</b>\n{utterance}"

        try:
            if send_to_telegram(message):
                text = "Сообщение записано!"
        except Exception as e:
            print(f"Telegram error: {str(e)}")
            text = "Извините, произошла ошибка при записи сообщения. Попробуйте позже."

    except ValueError as e:
        print(f"Validation error: {str(e)}")
        text = "Извините, произошла ошибка обработки запроса"
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        text = "Извините, произошла непредвиденная ошибка"

    return {
        "version": event["version"],
        "session": event["session"],
        "response": {"text": text, "end_session": "false"},
    }
