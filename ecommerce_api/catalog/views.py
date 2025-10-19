# catalog/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, BooleanFilter, CharFilter
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsAuthenticatedToManage

class ProductFilter(FilterSet):
    category = NumberFilter(field_name="category_id")
    category_slug = CharFilter(field_name="category__slug", lookup_expr="iexact")
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = BooleanFilter(method="filter_in_stock")

    def filter_in_stock(self, qs, name, value):
        return qs.filter(stock_qty__gt=0) if value else qs

    class Meta:
        model = Product
        fields = ("category","category_slug","min_price","max_price","in_stock","is_active")

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedToManage,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ("name", "category__name")     # partial matches supported
    ordering_fields = ("created_at","price","name","stock_qty")

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedToManage,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name","slug")
    ordering_fields = ("name","created_at")
