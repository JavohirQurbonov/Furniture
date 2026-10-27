from rest_framework import generics,filters
from apps.catalog.models import Category, Product
from apps.catalog.serializers import CategorySerializer, ProductSerializer


# Create your views here.

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name_uz','name_ru','name_en','description_uz']
    ordering_fields = ['price','created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category')
        category = self.request.query_params.get('category')
        if category:
            # slug yoki id
            if category.isdigit():
                qs = qs.filter(category_id=category)
            else:
                qs = qs.filter(category__slug=category)
        if self.request.query_params.get('is_featured') == 'true':
            qs = qs.filter(is_featured=True)
        return qs

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active = True)
    serializer_class = ProductSerializer