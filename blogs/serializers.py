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
    author = CharField(source='author.user_info.get_full_name')
    category = SimpleCategorySerializer(many=True)
    post_image_url = SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_post_image_url(self, obj):
        return obj.post_image.url if obj.post_image else None
