"""
Переопределение runserver: по умолчанию HTTPS (runserver_plus).
Браузер открывает https://127.0.0.1:8000/ — сервер должен поддерживать HTTPS.
"""
from django_extensions.management.commands.runserver_plus import Command as RunserverPlusCommand


class Command(RunserverPlusCommand):
    """runserver с HTTPS по умолчанию (--cert-file cert)."""
    help = 'Запуск dev-сервера по HTTPS. Поддержка https://127.0.0.1:8000/'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--no-https',
            action='store_true',
            help='Запустить по HTTP (без SSL)',
        )

    def handle(self, *args, **options):
        if not options.get('no_https') and not options.get('cert_path') and not options.get('key_file_path'):
            options['cert_path'] = 'cert'
        return super().handle(*args, **options)
