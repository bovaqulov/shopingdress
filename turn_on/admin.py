from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order, Gallery, OrderProduct, Product, Category, UserTelegram, ShippingAddress




class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "title",
    inlines = [GalleryInline]

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f"<img src='{obj.images.all()[0].image.url}' width='75'")
            except:
                return '-'
        return '-'


admin.site.register(Category)
admin.site.register(UserTelegram)

