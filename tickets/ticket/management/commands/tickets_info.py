# ваше_приложение/management/commands/ticket_commands.py
from django.core.management.base import BaseCommand
from django.db.models import Sum

from ...models import Ticket, Order

class Command(BaseCommand):
    help = 'Show info about all tickets'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, help='ID события')

    def handle(self, *args, **options):
        event_id = options['event_id']

        try:
            tickets_available = Ticket.objects.filter(
                event_id=event_id,
                quantity_available__gt=0
            ).aggregate(Sum('quantity_available'))['quantity_available__sum'] or 0

            total_orders = Order.objects.filter(event_id=event_id).count()

            self.stdout.write(self.style.SUCCESS(f'Доступно билетов: {tickets_available}'))
            self.stdout.write(self.style.SUCCESS(f'Общее количество заказов: {total_orders}'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Произошла ошибка: {e}'))
