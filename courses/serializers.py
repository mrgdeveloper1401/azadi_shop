from rest_framework import serializers
from courses.models import Course, CourseCategory, DiscountCourse, Comment


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class CourseDiscountSerializers(serializers.ModelSerializer):
    class Meta:
        model = DiscountCourse
        fields = '__all__'

        extra_kwargs = {
            'expired_date': {
                'format': '%Y-%m-%dT%H:%M',  # فرمت خروجی
                'input_formats': ['%Y-%m-%dT%H:%M']  # فرمت ورودی
            }
        }


class CommentSerializers(serializers.ModelSerializer):
    # course = CourseSerializers(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['id', 'user', 'body', 'admin_response', 'created', 'updated', 'public']
        # read_only_fields = ['created', 'updated', 'admin_response']


class CourseSerializers(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=CourseCategory.objects.all())
    # id = serializers.IntegerField(read_only=True)
    # total_price = serializers.SerializerMethodField()
    # course_discount = CourseDiscountSerializers(many=True, read_only=True)
    # comment = CommentSerializers(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_total_price(self, obj):
        return obj.get_total_price