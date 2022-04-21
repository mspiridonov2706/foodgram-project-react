from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    def clean(self):
        if self.user == self.author:
            raise ValidationError('You cannot follow yourself')

    def __str__(self):
        text = f'{self.user} подписан на {self.author}'
        return text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'
            ),
        ]


class Ingredients(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название ингридиента',
    )
    measurement_unit = models.CharField(
        max_length=32,
        verbose_name='Еденица измерения',
    )

    class Meta:
        unique_together = [['name', 'measurement_unit']]


class Tags(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название тэга',
        unique=True,
    )
    color = models.CharField(
        max_length=32,
        verbose_name='Цвет тэга',
    )
    slug = models.SlugField(
        max_length=32,
        verbose_name='Слаг',
        unique=True,
    )


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipe',
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Тэг',
        related_name='recipe',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipesIngridients',
        verbose_name='Ингридиенты',
        related_name='recipe',
        related_query_name='recipe',
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='media/recipes/images/',
        blank=True,
        db_index=True,
    )
    text = models.TextField(
        max_length=256,
        verbose_name='Описание рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )


class RecipesIngridients(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipes_ingredients',
        related_query_name='recipes_ingredients',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipes_ingredients',
        related_query_name='recipes_ingredients',
    )
    amount = models.IntegerField(
        verbose_name='Количество ингридиента',
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite',
    )

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite',
    )

    def clean(self):
        if self.user == self.author:
            raise ValidationError('It is already your fav =)')

    def __str__(self):
        text = f'{self.user} - {self.recipe}'
        return text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            ),
        ]


class ShoppingCarts(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shoppingcarts',
    )

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shoppingcarts',
    )

    def clean(self):
        if self.user == self.author:
            raise ValidationError('It is already in your shopping')

    def __str__(self):
        text = f'{self.user} - {self.recipe}'
        return text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping'
            ),
        ]
