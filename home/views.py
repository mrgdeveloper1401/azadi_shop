from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course
from rest_framework.permissions import AllowAny
from rest_framework import status
from courses.serializers import CourseSerializers
from django.db.models import F, ExpressionWrapper, DecimalField, Case, When
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIRequestFactory


class NewCourseApiView(APIView):
    serializer_class = CourseSerializers
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Course.objects.select_related('professor', 'category').order_by('-created_at')[:7]
        ser_data = self.serializer_class(many=True, instance=queryset)
        return Response(ser_data.data, status.HTTP_200_OK)


class MoreSaleCourseApiView(APIView):
    serializer_class = CourseSerializers
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Course.objects.select_related('professor', 'category').order_by('-sales')[:7]
        ser_data = self.serializer_class(many=True, instance=queryset)
        return Response(ser_data.data, status.HTTP_200_OK)


class AllTabCourseApiView(APIView):
    serializers_classes = CourseSerializers
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        tab = request.query_params.get('tab', 'all')

        if tab == 'پرفروش ترین':
            courses = Course.objects.select_related('professor', 'category').order_by('-sales')  # پرفروش‌ترین‌ها
        elif tab == 'جدیدترین':
            courses = Course.objects.select_related('professor', 'category').order_by('-created_at')  # جدیدترین‌ها
        elif tab == 'بیشترین تخفیف':
            courses = Course.objects.annotate(discounted_price=ExpressionWrapper(
                Case(
                    When(course_discount__type='درصدی',
                         then=F('price') - (F('price') * F('course_discount__value') / 100)),
                    When(course_discount__type='مقدار', then=F('price') - F('course_discount__value')),
                    default=F('price'),
                    output_field=DecimalField()
                ),
                output_field=DecimalField()
            )
            ).filter(
                course_discount__is_active=True,
                course_discount__expired_date__gte=timezone.now()
            ).order_by('-discounted_price')  # مرتب‌سازی بر اساس قیمت تخفیف‌خورده
        else:
            courses = Course.objects.select_related('professor', 'category').all()  # همه دوره‌ها

        serializer = self.serializers_classes(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HomePageApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        factory = APIRequestFactory()

        new_course_url = reverse('home:new_course')
        new_course_request = factory.get(new_course_url)
        new_course_response = NewCourseApiView.as_view()(new_course_request).data

        more_sale_course_url = reverse('home:more_sale_course')
        more_sale_course_request = factory.get(more_sale_course_url)
        more_sale_course_response = MoreSaleCourseApiView.as_view()(more_sale_course_request).data

        all_course_url = reverse('home:all_tab_course')
        all_course_request = factory.get(all_course_url)
        all_course_response = AllTabCourseApiView.as_view()(all_course_request).data

        result = {
            'new_courses': new_course_response,
            'most_sold_courses': more_sale_course_response,
            'all_courses': all_course_response,
        }

        return Response(result, status=status.HTTP_200_OK)