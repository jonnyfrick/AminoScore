from django.contrib.auth.models import User, Group
from rest_framework import serializers

from amino_json_responder.models import Food, FoodCategory

class FoodCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FoodCategory
        fields = ['url', 'category_name', 'vegan', 'vegetarian']


class FoodSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Food
        fields = ['url','food_category', 'food_name', 'Histidine', 'Isoleucine', 'Leucine', 'Lysine', 'Methionine', 'Phenylalanine', 'Threonine', 'Tryptophan', 'Valine', 'Tyrosine', 'TotalEnergy']
