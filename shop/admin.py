from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
    #value is set automatically using other field here is name


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'price', 'stock', 'available', 'created_at',
        'updated_at'
    ]
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    #field in list_editable should compulsorily be in list_display

    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Product, ProductAdmin)
