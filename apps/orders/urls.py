from django.urls import path
from .views import (
    OrderCreateView, MyOrdersView, OrderCancelView,
    FavoriteListCreateView, FavoriteDeleteView,
)

urlpatterns = [
    path('orders/', OrderCreateView.as_view()),
    path('orders/my/', MyOrdersView.as_view()),
    path('orders/<int:pk>/cancel/', OrderCancelView.as_view()),
    path('favorites/', FavoriteListCreateView.as_view()),
    path('favorites/<int:product_id>/', FavoriteDeleteView.as_view()),
]