from django.core.management.base import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN
from bot.tg.dc import Message


class Command(BaseCommand):
    help = 'Запуск телеграмм-бота'
    tg_client = TgClient(TG_TOKEN)

    def handle_user(self, msg: Message):
        """ Проверка наличия пользователя в БД """
        user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.from_.id,
            tg_chat_id=msg.chat.id)

        if created:

            self.tg_client.send_message(chat_id=msg.chat.id, text='Привет!')
            user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Подтверди, пожалуйста, свой аккаунт. '
                     f'Для подтверждения необходимо ввести код: {user.verification_code} на сайте!')
        else:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Ты уже был!')

    def handle(self, *args, **options):
        offset = 0
        # tg_client = TgClient(TG_TOKEN)
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_user(item.message)
                # print(item.message)
