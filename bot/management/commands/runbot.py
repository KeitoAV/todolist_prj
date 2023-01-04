from django.core.management.base import BaseCommand
from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN


class Command(BaseCommand):
    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(TG_TOKEN)
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
