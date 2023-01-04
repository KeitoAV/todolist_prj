from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN

cl = TgClient(TG_TOKEN)
print(cl.get_updates(offset=0, timeout=60))
print(cl.send_message(512826648, 'hello'))
