from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import (  # noqa E501
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import ItemList
from ..serializers import ItemSerializer, UserSerializer

User = get_user_model()


class ItemApiPagination(PageNumberPagination):
    page_size = 5


class ItemAPIv2ViewSet(ModelViewSet):
    queryset = ItemList.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemApiPagination


@api_view()
def item_api_user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    serializer = UserSerializer(instance=user)

    return Response(serializer.data)
