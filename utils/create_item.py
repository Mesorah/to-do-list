from django.contrib.auth import get_user_model

from tdl.models import ItemList

User = get_user_model()


def create_user(username='test', password='test'):
    return User.objects.create_user(
        username=username, password=password
    )


def create_items(qtd=1):
    user = create_user()

    for item_range in range(qtd):
        ItemList.objects.create(
            name=f'item-{item_range}',
            user=user,
            completed=True
        )

    return user
