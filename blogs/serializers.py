from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from blogs.models import CategoryNode, Post, BlogPostImage


class CategoryNodeSerializer(ModelSerializer):
    children = SerializerMethodField()

    class Meta:
        model = CategoryNode
        exclude = ['created_at', "updated_at"]
        # fields = '__all__'

    def get_children(self, obj):
        if obj.parent:
            return [i.category_name for i in obj.children.all()]
        return []


class SimpleCategorySerializer(CategoryNodeSerializer):
    class Meta:
        model = CategoryNode
        fields = ['category_name']


class BlogPostImageSerializer(ModelSerializer):
    class Meta:
        model = BlogPostImage
        fields = '__all__'


class PostSerializer(ModelSerializer):
    # category = SimpleCategorySerializer()
    category = SerializerMethodField()
    images = SerializerMethodField()
    author = CharField(source='author.get_full_name')

    class Meta:
        model = Post
        fields = '__all__'

    def get_category(self, obj):
        return [i.category_name for i in obj.category.all()]

    def get_images(self, obj):
        return [i.image.image_url for i in obj.fk_blog_post.all()]

