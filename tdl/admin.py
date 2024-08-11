from django.contrib import admin
from tdl.models import ItemList


@admin.register(ItemList)
class ItemListAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'created_at')
