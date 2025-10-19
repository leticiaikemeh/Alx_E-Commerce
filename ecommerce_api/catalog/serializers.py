
from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id","name","slug","created_at")
        read_only_fields = ("id","created_at")

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ("id","name","description","price","category","category_name",
                  "stock_qty","image_url","is_active","created_at","updated_at")
        read_only_fields = ("id","created_at","updated_at")

    def validate(self, data):
        # enforce required fields on create
        if self.instance is None:
            for f in ("name","price","stock_qty","category"):
                if f not in data:
                    raise serializers.ValidationError({f: "This field is required."})
        if "price" in data and data["price"] < 0:
            raise serializers.ValidationError({"price": "Price cannot be negative."})
        return data
