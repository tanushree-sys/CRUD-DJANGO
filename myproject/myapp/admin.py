from django.contrib import admin
from .models import Item
# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display= ('title', 'created_by', 'created_at')
    list_filter= ('created_at',)
    search_fields= ('title', 'description')
