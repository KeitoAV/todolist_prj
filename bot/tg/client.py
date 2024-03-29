import requests

from bot.tg.dc import (
    GetUpdatesResponse,
    SendMessageResponse,
    get_updates_schema,
    send_message_schema
)


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        response = requests.get(self.get_url(f'getUpdates?timeout={timeout}&offset={offset}'))
        json_data = response.json()
        print(json_data)
        return get_updates_schema().load(json_data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        response = requests.get(self.get_url(f'sendMessage?chat_id={chat_id}&text={text}'))
        json_data = response.json()
        print(json_data)
        return send_message_schema().load(json_data)
