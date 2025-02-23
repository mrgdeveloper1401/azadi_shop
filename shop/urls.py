from decouple import config
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from shop.base import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # path("api_auth/", include("users.urls", namespace="users")),
    # path("api_course/", include("courses.urls", namespace="course")),
    # path("api_payment/", include("payments.urls", namespace="payments")),
    # path("api_order/", include("orders.urls", namespace="orders")),
    path('api/main_settings/', include('api.v1.main_settings.urls', namespace='v1_main_settings')),
    path('api/blog/', include("api.v1.blogs.urls", namespace='v1_blogs')),
    # path('images/', include('images.urls', namespace='images')),
    # swagger ui
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # api auth
    # path('api-auth/', include('rest_framework.urls')),
    # django ckeditor
    # path('ckeditor/', include('ckeditor_uploader.urls')),

    # jet admin url
    # path('jet_api/', include('jet_django.urls')),

]

api_admin = [
    # path('user_admin/', include('users.api_admin.urls', namespace='user_admin')),
    # path('professor_admin/', include('professors.api_admin.urls', namespace='professor_admin')),
    # path('payment_admin/', include('payments.api_admin.urls', namespace='payment_admin')),
    # path('order_admin/', include('orders.api_admin.urls', namespace='order_admin')),
    # path('main_setting_admin/', include('main_settings.api_admin.urls', namespace='main_setting_admin')),
    # path('image_admin/', include('images.api_admin.urls', namespace='image_admin')),
    # path('course_admin/', include('courses.api_admin.urls', namespace='course_admin')),
    # path('blog_admin/', include('blogs.api_admin.urls', namespace='blog_admin'))
]

# api admin
urlpatterns += api_admin

# admin settings
admin.site.index_title = 'پنل مدیریت'

debug_mode = config("DEBUG", default=False, cast=str)
if debug_mode:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
