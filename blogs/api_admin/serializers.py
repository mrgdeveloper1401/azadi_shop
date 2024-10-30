from django.core.validators import MinValueValidator
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer, IntegerField, SerializerMethodField

from ..models import CategoryNode, Post


class AdminCategoryBlogSerializer(ModelSerializer):
    parent = IntegerField(required=False, allow_null=True, validators=[MinValueValidator(1)])

    class Meta:
        model = CategoryNode
        fields = '__all__'
        extra_kwargs = {
            'path': {'required': False},
            "depth": {"required": False}
        }

    def create(self, validated_data):
        parent = validated_data.pop('parent')
        if parent is None:
            instance = CategoryNode.add_root(**validated_data)
        else:
            category_node = get_object_or_404(CategoryNode, id=parent)
            instance = category_node.add_child(**validated_data)
        return instance


class AdminPostBlogSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
