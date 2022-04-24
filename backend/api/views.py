import io

from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets, exceptions
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import IngredientsFilter, RecipeFilter
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    IngredientsSerializer,
    RecipesSerializer,
    RecipesSmallSerializer,
    SetPasswordSerializer,
    TagsSerializer,
    UserFullSerializer,
    UserSerializer,
    UserSubsribedSerializer,
)
from recipes.models import (
    Favorite,
    Ingredients,
    Recipes,
    ShoppingCarts,
    Subscribe,
    Tags,
    User,
)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'get_subscriptions':
            return UserFullSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.request.method == 'GET':
            return UserSubsribedSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def my_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        url_path='set_password',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def set_password(self, request):
        user = request.user
        data = request.data
        context = {'request': request}
        serializer = self.get_serializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['new_password']
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def get_subscriptions(self, request):
        user = request.user
        follow = user.follower.values_list('author_id', flat=True)
        queryset = User.objects.all().filter(id__in=follow)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserFullSerializer

    def create(self, request, user_id):
        current_user = request.user
        author = get_object_or_404(User, id=user_id)

        if current_user == author:
            data = {'errors': 'Нельзя подписаться на самого себя'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        is_subscribed = Subscribe.objects.filter(
            user=current_user, author=author).exists()

        if is_subscribed:
            data = {'errors': 'Вы уже подписаны на данного пользователя'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        Subscribe.objects.create(user=current_user, author=author)
        serializer = self.get_serializer(author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def delete(self, request, user_id):
        current_user = request.user
        author = get_object_or_404(User, id=user_id)

        is_subscribed = Subscribe.objects.filter(
            user=current_user, author=author).exists()

        if not is_subscribed:
            data = {'errors': 'Вы не подписаны на данного пользователя'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        Subscribe.objects.filter(user=current_user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter
    filterset_fields = ('name',)


class TagsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = (
        'author',
        'tags',
        'is_favorited',
        'is_in_shopping_cart',
    )


class FavoriteAndShoppingViewSet(mixins.CreateModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):

    queryset = Recipes.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RecipesSmallSerializer
    pagination_class = None


class FavoritesViewSet(FavoriteAndShoppingViewSet):

    def create(self, request, recipe_id):

        current_user = request.user
        recipe = get_object_or_404(Recipes, id=recipe_id)

        is_favorite = Favorite.objects.filter(
            user=current_user, recipe=recipe).exists()

        if is_favorite:
            data = {'errors': 'Вы уже любите этот рецепт!'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        Favorite.objects.create(user=current_user, recipe=recipe)
        serializer = self.get_serializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def delete(self, request, recipe_id):

        current_user = request.user
        recipe = get_object_or_404(Recipes, id=recipe_id)

        is_favorite = Favorite.objects.filter(
            user=current_user, recipe=recipe).exists()

        if not is_favorite:
            data = {'errors': 'Вы ещё не добавили данный рецепт в любимое'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.filter(user=current_user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingViewSet(FavoriteAndShoppingViewSet):

    def create(self, request, recipe_id):

        current_user = request.user
        recipe = get_object_or_404(Recipes, id=recipe_id)

        is_in_shopping_cart = ShoppingCarts.objects.filter(
            user=current_user, recipe=recipe).exists()

        if is_in_shopping_cart:
            data = {'errors': 'Рецепт уже в списке покупок!'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        ShoppingCarts.objects.create(user=current_user, recipe=recipe)
        serializer = self.get_serializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def delete(self, request, recipe_id):
        current_user = request.user
        recipe = get_object_or_404(Recipes, id=recipe_id)

        is_favorite = ShoppingCarts.objects.filter(
            user=current_user, recipe=recipe).exists()

        if not is_favorite:
            data = {'errors': 'Рецепта нет в вашем списке покупок'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        ShoppingCarts.objects.filter(user=current_user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):
    if request.user.is_anonymous:
        raise exceptions.AuthenticationFailed
    current_user = request.user

    values = ('recipe__ingredients__name',
              'recipe__ingredients__measurement_unit')
    annotate = Sum('recipe__recipes_ingredients__amount')
    data = current_user.shoppingcarts.values_list(*values).annotate(annotate)

    file = ''.join([f'{d[0].capitalize()} ({d[1]}) - {d[2]}\n' for d in data])
    file = io.BytesIO(str.encode(file))

    response = FileResponse(file, content_type='text/plain',
                            as_attachment=True, filename='shopping-list.txt')

    return response
