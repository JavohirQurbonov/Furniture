from rest_framework import serializers
from apps.catalog.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id','name','slug','image')

    def get_name(self,obj):
        return {
            'uz':obj.name_uz,
            'ru':obj.name_ru or obj.name_uz,
            'en':obj.name_en or obj.name_uz,
        }

    def get_image(self,obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ('id','name','description','price','old_price','image','images','category','is_new'
        ,'is_featured','created_at',)

    def get_name(self,obj):
        return {
            'uz':obj.name_uz,
            'ru':obj.name_ru or obj.name_uz,
            'en':obj.name_en or obj.name_uz,
        }

    def get_description(self,obj):
        return {
            'uz':obj.description_uz,
            'ru':obj.description_ru or obj.description_uz,
            'en':obj.description_en or obj.description_uz,
        }

    def get_image(self,obj):
        request = self.context.get('request')
        if obj.image or request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_images(self,obj):
        request = self.context.get('request')
        urls = []
        if obj.image and request:
            urls.append(request.build_absolute_uri(obj.image.url))
        for img in obj.images.all().order_by('order'):
            if request:
                urls.append(request.build_absolute_uri(img.image.url))
        return urls
    
