from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from .models import Recipe, Ingredient, Upvote
from .serializers import RecipeSerializer, IngredientSerializer, UpvoteSerializer, RecipeDetailSerializer, UserRegistrationSerializer

class RecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]


class IngredientCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CreateUpvoteView(generics.CreateAPIView):
    serializer_class = UpvoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        return Upvote.objects.filter(user=user, recipe=recipe)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted on this you silly goose!')
        user = self.request.user
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=user, recipe=recipe)

    
class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = [permissions.AllowAny]


class RecipeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(author=self.request.user, pk=kwargs['pk'])
        if recipe.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Hey there...this isn\'t your recipe!')

    def perform_update(self, serializer, **kwargs):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        if self.request.user != recipe.author:
            raise ValidationError('You can\'t update something that isn\'t yours!')
        serializer.save(user=self.request.user, recipe=recipe)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            data = {'token': token}
        else:
            data = serializer.errors
        return Response(data=data, status=201)


class LoginView(generics.CreateAPIView):
    serializer_class = AuthTokenSerializer

    def create(self, request):
        return ObtainAuthToken().post(request)