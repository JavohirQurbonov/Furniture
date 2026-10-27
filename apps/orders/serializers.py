from rest_framework import serializers
from apps.catalog.serializers import ProductSerializer
from apps.orders.models import OrderItem, Order, Favorite


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=12,decimal_places=0)

class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)
    address = serializers.CharField()
    phone = serializers.CharField(max_length=20)
    note = serializers.CharField(required=False,allow_blank=True)

class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source='product.id')

    class Meta:
        model = OrderItem
        fields = ('product_id','name','quantity','price')

    def get_name(self,obj):
        p = obj.product
        return {
            'uz':p.name_uz,
            'ru':p.name_ru or p.name_uz,
            'en':p.name_en or p.name_uz,
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    total_price = serializers.DecimalField(source='total',max_digits=14,decimal_places=0,read_only=True)

    class Meta:
        model = Order
        fields = ('id','items', 'address', 'phone', 'note',
            'status', 'total', 'total_price', 'created_at',)

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'product', 'product_id', 'created_at')