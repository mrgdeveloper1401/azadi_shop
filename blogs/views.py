from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from blogs.models import Post, CategoryNode
from blogs.serializers import PostSerializer, CategoryNodeSerializer
from blogs.paginations import BlogPagination


class CategoryNodeViewSet(ReadOnlyModelViewSet):
    queryset = CategoryNode.objects.all()
    serializer_class = CategoryNodeSerializer


class PostViewSet(ReadOnlyModelViewSet):
    queryset = (Post.objects.filter(is_publish=True).prefetch_related('category').
                select_related('author'))
    serializer_class = PostSerializer
    pagination_class = BlogPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['view_number', "created_at", "updated_at"]
    
    def get_queryset(self):
        if 'category_pk' in self.kwargs:
            return (Post.objects.filter(category=self.kwargs['category_pk']).
                    prefetch_related('category').select_related('author').
                    filter(is_publish=True))
        return super().get_queryset()


class ListPostViewSet(ListModelMixin, GenericViewSet):
    queryset = (Post.objects.filter(is_publish=True)
                .prefetch_related('category')
                .select_related('author')
                .order_by('-view_number')[:10])
    serializer_class = PostSerializer

    def get_queryset(self):
        if 'category_pk' in self.kwargs:
            return (Post.objects.filter(category=self.kwargs['category_pk'], is_publish=True)
                    .prefetch_related('category')
                    .select_related('author')
                    .order_by('-view_number')[:10])
        return super().get_queryset()
