# Generated by Django 2.2.19 on 2022-04-16 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20220416_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='image',
            field=models.ImageField(blank=True, db_index=True, upload_to='recipes/images/', verbose_name='Картинка'),
        ),
    ]
