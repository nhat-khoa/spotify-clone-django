from rest_framework.viewsets import ModelViewSet
from .models import Category, PodcastCategory
from .serializers import CategorySerializer, PodcastCategorySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PodcastCategoryViewSet(ModelViewSet):
    queryset = PodcastCategory.objects.all()
    serializer_class = PodcastCategorySerializer
