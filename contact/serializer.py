from rest_framework import serializers
from .models import Product
from django.utils.translation import gettext_lazy as _

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


