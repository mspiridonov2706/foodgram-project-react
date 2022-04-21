from django.contrib import admin

from .models import (
    Favorite,
    Ingredients,
    Recipes,
    RecipesIngridients,
    ShoppingCarts,
    Subscribe,
    Tags,
    User,
)


admin.site.unregister(User)


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorite_count',)

    def favorite_count(self, obj):
        count = obj.favorite.all().count()
        return count

    favorite_count.short_description = "Добавленно в избранное"


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    list_filter = ('email',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(RecipesIngridients)
class RecipesIngridientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe_id', 'recipe', 'ingredient', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


@admin.register(ShoppingCarts)
class ShoppingCartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
