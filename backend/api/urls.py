from django.urls import include, path
from rest_framework import routers

from api.auth import CustomAuthToken, CustomLogoutToken
from api.views import (
    FavoritesViewSet,
    IngredientsViewSet,
    RecipesViewSet,
    ShoppingViewSet,
    SubscribeViewSet,
    TagsViewSet,
    UserViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users/(?P<user_id>[\d]+)/subscribe',
                SubscribeViewSet,
                basename='subscribe')
router.register('users', UserViewSet)

router.register('ingredients', IngredientsViewSet)

router.register('tags', TagsViewSet)

router.register(r'recipes/(?P<recipe_id>[\d]+)/favorite',
                FavoritesViewSet,
                basename='recipes')
router.register(r'recipes/(?P<recipe_id>[\d]+)/shopping_cart',
                ShoppingViewSet,
                basename='shopping_cart')
router.register('recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', CustomAuthToken.as_view()),
    path('auth/token/logout/', CustomLogoutToken.as_view()),
]
