from django.core.validators import MinValueValidator
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField

from ..models import CourseCategory, Course, DiscountCourse, Comment


class AdminCategorySerializer(ModelSerializer):
    parent = IntegerField(required=False, validators=[MinValueValidator(1)])
    category_child = SerializerMethodField()

    class Meta:
        model = CourseCategory
        fields = '__all__'
        extra_kwargs = {
            "path": {"required": False},
            "depth": {'required': False},
        }

    def create(self, validated_data):
        parent = validated_data.pop('parent', None)
        if parent is None:
            instance = CourseCategory.add_root(**validated_data)
        else:
            category_node = get_object_or_404(CourseCategory, pk=parent)
            instance = category_node.add_child(**validated_data)
        return instance

    def get_category_child(self, obj):
        return obj.get_children().values('name')


class AdminCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AdminDiscountCourseSerializer(ModelSerializer):
    course_name = SerializerMethodField()

    class Meta:
        model = DiscountCourse
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name


class AdminCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
