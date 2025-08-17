from django.contrib import admin
from .models import Category,Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','slug']


@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','slug']