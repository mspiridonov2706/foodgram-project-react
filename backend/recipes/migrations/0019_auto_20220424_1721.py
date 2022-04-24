# Generated by Django 2.2.19 on 2022-04-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_auto_20220421_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Любимый рецепт', 'verbose_name_plural': 'Любимые рецепты'},
        ),
        migrations.AlterModelOptions(
            name='ingredients',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipes',
            options={'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipesingridients',
            options={'verbose_name': 'Рецепт-ингредиент', 'verbose_name_plural': 'Рецепты-ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcarts',
            options={'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterModelOptions(
            name='tags',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
        migrations.AlterUniqueTogether(
            name='ingredients',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='ingredients',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient'),
        ),
    ]