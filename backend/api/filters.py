from django_filters import rest_framework as filters

from recipes.models import Ingredients, Recipes


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='exact',
        method='filter_tags',
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='filter_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart',
    )

    def filter_tags(self, queryset, name, value):
        tags = self.data.getlist('tags')
        for tag in tags:
            queryset = queryset.filter(tags__slug=tag)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value:
            current_user = self.request.user
            queryset = queryset.filter(favorite__user=current_user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            current_user = self.request.user
            queryset = queryset.filter(shoppingcarts__user=current_user)
        return queryset

    class Meta:
        model = Recipes
        fields = ['tags', 'is_favorited']


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',
                              method='name_filter')

    class Meta:
        model = Ingredients
        fields = ['name']

    def name_filter(self, queryset, name, value):
        queryset = queryset.filter(name__iregex=rf'^{value}')
        return queryset
