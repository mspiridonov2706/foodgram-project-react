from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'
            ),
        ]

        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписываться на самого себя.')

    def __str__(self):
        str = f'{self.user} подписан на {self.author}'
        return str


class Ingredients(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=32,
        verbose_name='Еденица измерения',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            ),
        ]

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


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
        verbose_name='Ингредиенты',
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
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                limit_value=0,
                message='Время приготовления не может быть отрицательным',
            )
        ],
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name


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
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(
                limit_value=0,
                message='Кол-во ингредиента не может быть отрицательным',
            )
        ],
    )

    class Meta:
        verbose_name = 'Рецепт-ингредиент'
        verbose_name_plural = 'Рецепты-ингредиенты'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            ),
        ]

        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'

    def __str__(self):
        text = f'{self.user} - {self.recipe}'
        return text


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping'
            ),
        ]

        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Рецепт уже в списке покупок.')

    def __str__(self):
        text = f'{self.user} - {self.recipe}'
        return text
