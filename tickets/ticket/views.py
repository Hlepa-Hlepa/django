from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .models import Event, Ticket, Order
from .pagination import TicketPagination, OrderPagination, EventPagination
from .serializers import EventSerializer, TicketSerializer, OrderSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination
    filter_backends = [SearchFilter]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = TicketPagination
    filter_backends = [SearchFilter]

    @action(methods=['post'], detail=True)
    def perform_ticket_create(self, request, pk=None):
        ticket = self.get_object()
        if ticket.quantity_available > 0:
            ticket.quantity_sold += 1
            ticket.save()
            order = Order.objects.create(
                event=ticket.event,
                ticket=ticket,
                quantity=1,
                total_price=ticket.price
            )
            return Response({'success': True, 'message': 'Order created successfully'})
        else:
            return Response({'success': False, 'message': 'No available tickets'})

    @action(methods=['get'], detail=False)
    def filter_tickets(self, request):
        event_id = request.query_params.get('event_id')
        max_price = request.query_params.get('max_price', 40000)

        if not event_id:
            return Response({'error': 'Параметр event_id обязателен'}, status=400)

        try:
            event_id = int(event_id)
            max_price = float(max_price)
        except ValueError:
            return Response({'error': 'Некорректные значения параметров'}, status=400)

        tickets = Ticket.objects.filter(
            (Q(event_id=event_id) & ~Q(price__gt=max_price)) | (Q(event_id=event_id) & Q(ticket_type='economy'))
        )

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)




class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [SearchFilter]

    @action(methods=['get'], detail=False)
    def filter_orders(self, request):
        event_id = request.query_params.get('event_id')
        max_total_price = request.query_params.get('max_total_price', 40000)

        if not event_id:
            return Response({'error': 'Параметр event_id обязателен'}, status=400)

        try:
            event_id = int(event_id)
            max_total_price = float(max_total_price)
        except ValueError:
            return Response({'error': 'Некорректные значения параметров'}, status=400)

        orders = Order.objects.filter(
            (Q(event_id=event_id) & ~Q(total_price__gt=max_total_price)) | (Q(event_id=event_id) & Q(quantity__gt=1))
        )

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)



