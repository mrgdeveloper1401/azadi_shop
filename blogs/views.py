from rest_framework.viewsets import ReadOnlyModelViewSet

from blogs.models import Post, CategoryNode
from blogs.serializers import PostSerializer, CategoryNodeSerializer
from blogs.paginations import BlogPagination


class CategoryNodeViewSet(ReadOnlyModelViewSet):
    queryset = CategoryNode.objects.all()
    serializer_class = CategoryNodeSerializer
    lookup_field = 'category_slug'


class PostViewSet(ReadOnlyModelViewSet):
    queryset = (Post.objects.filter(is_publish=True).prefetch_related('category').
                select_related('author'))
    serializer_class = PostSerializer
    pagination_class = BlogPagination
    lookup_field = 'slug'

    def get_queryset(self):
        if self.kwargs:
            return (Post.objects.filter(category__category_slug=self.kwargs['category_category_slug']).
                    prefetch_related('category').select_related('author').
                    filter(is_publish=True))
        return super().get_queryset()
