from rest_framework import serializers
from .models import *
from rest_framework.fields import ReadOnlyField
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        product = Product.objects.create(
            author=request.user,
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            image=validated_data.get('image'),
            shop=validated_data.get('shop'),
            category=validated_data.get('category'),
            status=validated_data.get('status'),
            price=validated_data.get('price')
        )
        return product

class ShopSerializer(serializers.ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Shop
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        shop = Shop.objects.create(
            author=request.user,
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            image=validated_data.get('image'),
            address=validated_data.get('address')
        )
        return shop
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["products"] = ProductSerializer(instance.products.all(),
                                                       context=self.context,
                                                       many=True).data
        return representation