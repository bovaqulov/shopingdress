from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **options):
        from botapp.bot_main.loader import bot
        print('Bot ishladi...')
        bot.infinity_polling()
