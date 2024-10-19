from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from blogs.models import CategoryNode, Post


class CategoryNodeSerializer(ModelSerializer):

    class Meta:
        model = CategoryNode
        fields = ['id', "category_name", "category_slug", "path", "depth", 'numchild', "children"]


class SimpleCategorySerializer(CategoryNodeSerializer):
    class Meta:
        model = CategoryNode
        fields = ['category_name']


class PostSerializer(ModelSerializer):
    author = CharField(source='author.get_full_name')
    category = SimpleCategorySerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
