from django.contrib import admin
from tdl.models import ItemList, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemList)
class ItemListAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'created_at')
