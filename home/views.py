from django.utils import timezone
from django.db.models import OuterRef, Subquery, F, DecimalField, ExpressionWrapper, Case, When, Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import Course, DiscountCourse
from courses.serializers import CourseSerializers


class HomePageApiView(APIView):
    """
    ویو برای نمایش داده‌های صفحه اصلی شامل:
    - جدیدترین دوره‌ها
    - پرفروش‌ترین دوره‌ها
    - تفکیک دوره‌ها براساس تب
    """

    serializer_class = CourseSerializers

    def get(self, request):
        courses = Course.objects.select_related('professor', "professor__professor_image", 'category',
                                                'image').annotate(
            discount_amount=Subquery(
                DiscountCourse.objects.filter(
                    course=OuterRef('pk'),
                    is_active=True,
                    expired_date__gte=timezone.now()
                ).order_by('-created_at').values('value')[:1]
            ),
            discount_type=Subquery(
                DiscountCourse.objects.filter(
                    course=OuterRef('pk'),
                    is_active=True,
                    expired_date__gte=timezone.now()
                ).order_by('-created_at').values('discount_type')[:1]
            ),
            final_price=Case(
                When(discount_type='درصدی', then=ExpressionWrapper(
                    F('price') - (F('price') * F('discount_amount') / 100),
                    output_field=DecimalField()
                )),
                When(discount_type='مقدار', then=ExpressionWrapper(
                    F('price') - F('discount_amount'),
                    output_field=DecimalField()
                )),
                default=F('price'),
                output_field=DecimalField()
            )
        )

        latest_courses = courses.order_by('-created_at')[:8]

        most_sold_courses = courses.order_by('-sale_number')[:8]

        tab = request.query_params.get('tab', 'all')

        if tab == 'جدیدترین':
            filtered_courses = latest_courses
        elif tab == 'پرفروش‌ترین':
            filtered_courses = most_sold_courses
        elif tab == 'بیشترین تخفیف':
            filtered_courses = courses.filter(
                Q(discount_amount__isnull=False) & Q(discount_amount__gt=0)
            ).order_by('-discount_amount')[:8]
        else:
            filtered_courses = courses

        result = {
            'latest_courses': self.serializer_class(latest_courses, many=True).data,
            'most_sold_courses': self.serializer_class(most_sold_courses, many=True).data,
            'filtered_courses': self.serializer_class(filtered_courses, many=True).data,
        }

        return Response(result, status=status.HTTP_200_OK)


class MostSoldCourseApiView(APIView):
    def get(self, request):
        q = (Course.objects.select_related("professor", "professor__professor_image", 'category', "image").
             prefetch_related("course_discount")).annotate(
            dicount=DiscountCourse.objects.filter(is_active=True, expired_date__gte=timezone.now()).
                    order_by('-sale_number')[:8]
        )
        ser_data = CourseSerializers(q, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def get(self, request):
        pass
