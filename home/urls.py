from django.urls import path
from .views import NewCourseApiView, AllTabCourseApiView, MoreSaleCourseApiView, HomePageApiView


app_name = 'home'
urlpatterns = [
    path('', HomePageApiView.as_view(), name='homepage'),
    path('new_course/', NewCourseApiView.as_view(), name='new_course'),
    path('mor_sale_course/', MoreSaleCourseApiView.as_view(), name='more_sale_course'),
    path('all_course/', AllTabCourseApiView.as_view(), name='all_tab_course'),
]
