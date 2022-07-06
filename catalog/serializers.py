from rest_framework import serializers
from catalog.models import Product, Tag, Category, Review
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagListSerializer(many=True)
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'category id title price price_som tags tag_list tag_list_2'.split()

    def get_tag_list(self, product):
        return [i.name for i in product.tags.all()]


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text author created_at stars'.split()


class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True)
    custom_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id rating title price tag_list_2 reviews custom_reviews'.split()

    def get_custom_reviews(self, product):
        data = product.reviews.all()
        # data = Review.objects.filter(product=product)
        return ReviewListSerializer(data, many=True).data


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=12)
    description = serializers.CharField(required=False)
    prise = serializers.FloatField(min_value=0.5, max_value=1000000)
    category = serializers.IntegerField(required=False,
                         allow_null=True, default=None)
    tags = serializers.ListField(child=serializers.IntegerField())

    @property
    def product_data_witho_out_tags(self):
        dict_ = {
            'title': self.validated_data.get('title'),
            'price': self.validated_data.get('price'),
            'description': self.validated_data.get('description'),
            'category_id': self.validated_data.get('category'),
        }
        return dict_

    # def validate_category(self, category):
    #     try:
    #         category.objects.get(id=category)
    #     except:
    #         raise ValidationError('Category not found!!/ Глаза открой дебил, такой категорий не существует!')
    #
    def validate_category(self, category):
        if Category.objects.filter(id=category).count() == 0:
            raise ValidationError('Category not found!')
        return category
    def validate_tags(self, tags):
        tag_list = Tag.objects.filter(id__in=tags)
        if len(tags)!=tag_list.count():
            raise ValidationError
        print(tags)
        return tags

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exist!')
