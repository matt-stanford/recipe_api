from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from recipes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/recipes/', views.RecipeListView.as_view()),
    path('api/recipes/create/', views.RecipeCreateView.as_view()),
    path('api/recipes/<int:pk>', views.RecipeDetailView.as_view()),
    path('api/recipes/<int:pk>/update/', views.RecipeUpdateView.as_view()),
    path('api/recipes/<int:pk>/upvote/', views.CreateUpvoteView.as_view()),
    path('api/ingredients/', views.IngredientCreateView.as_view()),
    path('api/register/', views.UserRegistrationView.as_view()),
    path('api/login/', views.LoginView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
