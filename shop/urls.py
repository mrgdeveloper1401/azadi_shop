from decouple import config
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from debug_toolbar.toolbar import debug_toolbar_urls
from shop.base import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

# url order panel api_admin
# admin_url = [
#     path('order/', include('orders.api_admin.urls', namespace='admin_order')),
#     path('auth_admin/', include('users.api_admin.urls'))
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api_auth/", include("users.urls", namespace="users")),
    path("api_course/", include("courses.urls", namespace="course")),
    path("api_payment/", include("payments.urls", namespace="payments")),
    path("api_order/", include("orders.urls", namespace="orders")),
    path('api_main_settings/', include('main_settings.urls', namespace='main_settings')),
    path('api_blog/', include("blogs.urls", namespace='blogs')),
    # path('images/', include('images.urls', namespace='images')),
    # swagger ui
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # api auth
    path('api-auth/', include('rest_framework.urls')),
    # django ckeditor
    # path("ckeditor5/", include('django_ckeditor_5.urls')),

]

debug_mode = config("DEBUG", default=True, cast=str)
if debug_mode:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
