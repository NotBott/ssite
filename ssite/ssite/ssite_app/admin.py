from django.contrib import admin

from . import models


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage
    extra = 1
    max_num = 10


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    inlines = [
        ProductImageInline
    ]


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category)
admin.site.register(models.Basket)
admin.site.register(models.Favorites)
admin.site.register(models.Comment)
admin.site.register(models.UserVisit)
