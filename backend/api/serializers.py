import base64
import io
import uuid

from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework import serializers

from recipes.models import (
    Ingredients,
    Recipes,
    RecipesIngridients,
    Tags,
    User,
)


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,)
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    first_name = serializers.CharField(
        max_length=150,
        required=True,
    )
    last_name = serializers.CharField(
        max_length=150,
        required=True,
    )
    password = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists!")
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists!")
        return username


class UserSubsribedSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and obj.following.filter(user=user.id):
            return True
        return False


class RecipesSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['id', 'name', 'image', 'cooking_time']


class UserFullSerializer(UserSubsribedSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSubsribedSerializer.Meta):
        fields = UserSubsribedSerializer.Meta.fields + ['recipes',
                                                        'recipes_count']

    def get_recipes(self, user):
        limit = self.context['request'].query_params.get('recipes_limit')
        if limit:
            queryset = Recipes.objects.filter(author=user)[:int(limit)]
        else:
            queryset = user.recipe
        recipes = RecipesSmallSerializer(queryset, many=True).data
        return recipes

    def get_recipes_count(self, user):
        count = user.recipe.count()
        return count


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        required=True,
        max_length=150,
        write_only=True,
    )
    current_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate_new_password(self, password):
        user = self.context['request'].user
        validate_password(password, user)
        return password

    def validate_current_password(self, password):
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError("Текущий пароль указан неверно!")
        return password

    def validate(self, data):
        new_password = data['new_password']
        current_password = data['current_password']
        if current_password == new_password:
            raise serializers.ValidationError("Пароли не должны совпадать")
        return data


class IngredientsSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'measurement_unit', 'amount']
        read_only_fields = ['name', 'measurement_unit']


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ['id', 'name', 'color', 'slug']


class IngredientsRecipeSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = RecipesIngridients
        fields = ('id', 'amount', 'name', 'measurement_unit')
        read_only_fields = ['name', 'measurement_unit']

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipesSerializer(serializers.ModelSerializer):

    image = serializers.ImageField()
    ingredients = IngredientsSerializer(many=True)
    author = UserSubsribedSerializer(default=serializers.CurrentUserDefault())
    is_favorited = serializers.SerializerMethodField(required=False)
    is_in_shopping_cart = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Recipes
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def to_internal_value(self, data):
        if not data.get('image'):
            return super(RecipesSerializer, self).to_internal_value(data)
        image = data['image'].split(',')[-1]
        decoded_file = base64.b64decode(image)

        image_stream = io.BytesIO(decoded_file)
        image = Image.open(image_stream)

        file_name = str(uuid.uuid4())
        filetype = image.format

        data['image'] = ContentFile(
            decoded_file,
            name=file_name + '.' + filetype
        )

        return super(RecipesSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["tags"] = TagsSerializer(instance.tags.all(), many=True).data
        rep["ingredients"] = IngredientsRecipeSerializer(
            instance.recipes_ingredients.all(), many=True).data
        return rep

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipes.objects.create(**validated_data)

        recipe.tags.set(tags)

        for ingredient in ingredients:
            current_ingredient = Ingredients.objects.filter(
                id=ingredient['id'].id).first()
            RecipesIngridients.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, recipe, validated_data):
        tags = None
        ingredients = None

        # update tags
        if validated_data.get('tags'):
            tags = validated_data.pop('tags')
            recipe.tags.set(tags)

        # update ingredients
        if validated_data.get('ingredients'):
            ingredients = validated_data.pop('ingredients')
        if ingredients:
            for i in RecipesIngridients.objects.filter(recipe_id=recipe.id):
                i.delete()
            for ingredient in ingredients:
                current_ingredient = Ingredients.objects.filter(
                    id=ingredient['id'].id).first()
                RecipesIngridients.objects.create(
                    ingredient=current_ingredient,
                    recipe=recipe,
                    amount=ingredient['amount']
                )

        # update all remaining fields
        for key, value in validated_data.items():
            setattr(recipe, key, value)
        recipe.save()
        return recipe

    def get_is_favorited(self, recipe):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        is_favorited = current_user.favorite.filter(
            user=current_user.id,
            recipe=recipe.id
        )
        if is_favorited:
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        is_in_shopping_cart = current_user.shoppingcarts.filter(
            user=current_user.id,
            recipe=recipe.id
        )
        if is_in_shopping_cart:
            return True
        return False
