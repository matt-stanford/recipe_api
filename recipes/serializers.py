from rest_framework import serializers
from django.db.models import Sum
from django.contrib.auth.models import User

from .models import Recipe, Ingredient, Upvote

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())
    total_calories = serializers.SerializerMethodField()
    upvotes = serializers.SerializerMethodField()

    def get_total_calories(self, recipe):
        return Ingredient.objects.filter(recipe=recipe).aggregate(Sum('calories'))

    def get_upvotes(self, recipe):
        return Upvote.objects.filter(recipe=recipe).count()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'title', 'image', 'time_mins', 'ingredients', 'total_calories', 'diet', 'upvotes', 'created', 'updated')
        read_only_fields = ('id', 'author')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'calories')
        read_only_fields = ('id',)


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ('id',)
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user