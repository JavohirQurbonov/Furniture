from decimal import Decimal
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.catalog.models import Product
from apps.common.telegram import notify_order_cancelled, notify_new_order
from apps.orders.models import Order, OrderItem, Favorite
from apps.orders.serializers import OrderCreateSerializer, OrderSerializer, FavoriteSerializer
from apps.users.models import User


# Create your views here.

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        ser = OrderCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        order = Order.objects.create(
            user = request.user,
            address = data['address'],
            phone = data['phone'],
            note = data.get('note','')
        )

        total = Decimal('0')
        for item in data['items']:
            product = Product.objects.get(pk = item['product_id'])
            price = item.get('price') or product.price
            OrderItem.objects.create(
                order = order,
                product = product,
                quantity = item['quantity'],
                price = price
            )
            total+=price*item['quantity']
        order.total = total
        order.save(update_fields=['total'])
        notify_new_order(order)
        return Response(OrderSerializer(order, context={'request': request}).data,
            status=status.HTTP_201_CREATED,)

class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        orders = Order.objects.filter(user = request.user).prefetch_related('items__product')
        ser = OrderSerializer(orders,many=True,context={
            'request':request
        })
        return Response(ser.data)

class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        try:
            order = Order.objects.get(pk = pk,user = request.user)
        except Order.DoesNotExist:
            return Response({'detail':'Topilmadi'},status=status.HTTP_404_NOT_FOUND)

        if order.status not in ('pending','new'):
            return Response({'detail':'Buyurtmani bekor qilib bo\'lmaydi'},status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save(update_fields = ['status','updated_at'])
        notify_order_cancelled(order)
        return Response(OrderSerializer(order).data)

class FavoriteListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        favs = Favorite.objects.filter(user = request.user).select_related('product')
        ser = FavoriteSerializer(favs,many=True,context={'request':request})
        return Response(ser.data)

    def post(self,request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'detail':'product_id kerak'},status=status.HTTP_400_BAD_REQUEST)

        fav,created = Favorite.objects.get_or_create(
            user = request.user, product_id = product_id
        )
        ser = FavoriteSerializer(fav,context={'request':request})
        return Response(ser.data,status=201 if created else 200)

class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,product_id):
        Favorite.objects.filter(user = request.user,product_id = product_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







