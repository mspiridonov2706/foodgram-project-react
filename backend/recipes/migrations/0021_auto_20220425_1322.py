# Generated by Django 2.2.19 on 2022-04-25 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_auto_20220425_1252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipes',
            options={'ordering': ['-id'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
    ]
