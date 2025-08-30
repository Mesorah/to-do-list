from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import ItemList
from ..serializers import ItemSerializer, UserSerializer

User = get_user_model()


@api_view(http_method_names=['GET', 'POST'])
def item_api_list(request):
    if request.method == 'GET':
        items = ItemList.objects.all()[:10]

        serializer = ItemSerializer(
            instance=items,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view(http_method_names=['GET', 'PATCH', 'DELETE'])
def item_api_detail(request, pk):
    item = get_object_or_404(ItemList, pk=pk)

    if request.method == 'GET':
        serializer = ItemSerializer(
            instance=item,
            context={'request': request}
        )

        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = ItemSerializer(
            instance=item,
            data=request.data,
            context={'request': request},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def item_api_user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    serializer = UserSerializer(instance=user)

    return Response(serializer.data)
