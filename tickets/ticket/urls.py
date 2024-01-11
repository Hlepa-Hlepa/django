from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, TicketViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('api/', include(router.urls))
]
