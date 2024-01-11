from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from rest_framework.reverse import reverse
from simple_history.admin import SimpleHistoryAdmin

from .models import Event, Ticket, Order



class EventResource(resources.ModelResource):
    class Meta:
        model = Event


class TicketResource(resources.ModelResource):
    class Meta:
        model = Ticket

    def dehydrate_price(self, ticket):
        return f'{round(ticket.price,2)}руб.'


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order

#inlines
class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1

class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
#inlines

class EventAdmin(ExportMixin,SimpleHistoryAdmin):
    resource_class = EventResource
    list_display = ('title', 'date_time', 'location')
    list_filter = ('date_time',)
    search_fields = ('title', 'location')
    inlines = [TicketInline, OrderInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Event Details', {
            'fields': ('date_time', 'location'),
            'classes': ('collapse',),
        }),

    )


class TicketAdmin(ExportMixin,SimpleHistoryAdmin):
    resource_class = TicketResource
    list_display = ('ticket_type', 'event_link', 'price', 'quantity_available', 'quantity_sold')
    list_filter = ('event',)
    search_fields = ('ticket_type', 'event__title')
    fieldsets = (
        (None, {
            'fields': ('ticket_type', 'event')
        }),
        ('Ticket Details', {
            'fields': ('price', 'quantity_available', 'quantity_sold'),
            'classes': ('collapse',),
        }),

    )

    def get_export_queryset(self, request):
        return Ticket.objects.filter(quantity_available__gt=0)

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


    def event_link(self, obj):
        url = reverse('admin:ticket_event_change', args=[obj.event.id])
        return format_html('<a href="{}">{}</a>', url, obj.event.title)

    event_link.short_description = 'Event'


class OrderAdmin(ExportMixin,SimpleHistoryAdmin):
    resource_class = OrderResource
    list_display = ('event_link', 'ticket_link', 'quantity', 'total_price')
    list_filter = ('event',)
    search_fields = ('event__title', 'ticket__ticket_type')
    fieldsets = (
        (None, {
            'fields': ('event', 'ticket')
        }),
        ('Order Details', {
            'fields': ('quantity', 'total_price'),
            'classes': ('collapse',),
        }),

    )


    def event_link(self, obj):
        url = reverse('admin:ticket_event_change', args=[obj.event.id])
        return format_html('<a href="{}">{}</a>', url, obj.event.title)

    event_link.short_description = 'Event'

    def ticket_link(self, obj):
        url = reverse('admin:ticket_ticket_change', args=[obj.ticket.id])
        return format_html('<a href="{}">{}</a>', url, obj.ticket.ticket_type)

    ticket_link.short_description = 'Ticket'


# Register your models here.
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Order, OrderAdmin)
