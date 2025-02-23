from rest_framework import serializers

from blogs.models import CategoryNode, Post


class CategoryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNode
        exclude = ['created_at', "updated_at", "is_deleted", "deleted_at", "is_active"]


class SimpleCategorySerializer(CategoryNodeSerializer):
    class Meta:
        model = CategoryNode
        fields = ['category_name']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.user_info.get_full_name')
    category = SimpleCategorySerializer(many=True)

    class Meta:
        model = Post
        exclude = ['deleted_at', "is_deleted"]
