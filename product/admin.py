from django.contrib import admin

from product.models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'date_added',)
    prepopulated_fields = {'slug': ('name', 'category')}


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
