from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tdl.permissions import IsOwner

from ..models import ItemList
from ..serializers import ItemSerializer, UserSerializer

User = get_user_model()


class ItemApiPagination(PageNumberPagination):
    page_size = 5


class ItemAPIViewSet(ModelViewSet):
    queryset = ItemList.objects.all().order_by('-id')
    serializer_class = ItemSerializer
    pagination_class = ItemApiPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner()]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view()
def item_api_user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    serializer = UserSerializer(instance=user)

    return Response(serializer.data)
