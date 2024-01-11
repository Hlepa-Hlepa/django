from datetime import timezone

from rest_framework import serializers
from .models import Event, Ticket, Order

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата и время мероприятия не могут быть в прошлом.")
        return value

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def validate_quantity_available(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество доступных билетов должно быть неотрицательным числом.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество заказанных билетов должно быть неотрицательным числом.")
        return value
