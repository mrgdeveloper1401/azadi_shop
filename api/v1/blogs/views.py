from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.filters import OrderingFilter
from rest_framework import mixins
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from django.db.models import Prefetch

from blogs.models import Post, CategoryNode
from . import serializers
from . import paginations


class CategoryNodeViewSet(ReadOnlyModelViewSet):
    queryset = CategoryNode.objects.filter(is_active=True).only(
        'id', "category_name", "numchild", "path", "depth"
    )
    serializer_class = serializers.CategoryNodeSerializer

    @method_decorator(cache_page(20 * 60, key_prefix="category_list_cache"))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    @method_decorator(cache_page(20 * 60, key_prefix="category_retrieve_cache"))
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response


class PostViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.PostSerializer
    pagination_class = paginations.BlogPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['view_number', "created_at", "updated_at"]
    
    def get_queryset(self):
        return (Post.objects.filter(is_publish=True).
                prefetch_related(
            Prefetch("category", CategoryNode.objects.filter(is_active=True).only("category_name"))
        ).select_related("author__user_info").only(
            "id", "author__user_info__first_name", "author__user_info__last_name", "category", "post_image",
            "created_at", "updated_at", "post_title", "tiny_title", "introduction", "slug", "post",
            "is_publish", "view_number"
        ))

    @method_decorator(cache_page(20 * 60, key_prefix="post_list_cache"))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    @method_decorator(cache_page(20 * 60, key_prefix="post_retrieve_cache"))
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response
