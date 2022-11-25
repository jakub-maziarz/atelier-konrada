from django.contrib import admin
from shop.models import *
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class ImageAdminInline(admin.TabularInline):
    model = Image


class CategoryProductAdminInline(admin.TabularInline):
    model = CategoryProduct
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageAdminInline, CategoryProductAdminInline)
    list_display = ('name', 'status')
    search_fields = ('name',)
    actions = ['change_status']

    def change_status(self, request, queryset):
        for item in queryset:
            item.status = not item.status
            item.save()
            self.message_user(
                request, f'Produkt \"{item}\" został pomyślnie zmieniony.', messages.SUCCESS)
            self.log_change(
                request, item, 'Zmodyfikowano Status.')
    change_status.short_description = _("Change Status")


class OrderProductAdminInline(admin.TabularInline):
    model = OrderProduct


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderProductAdminInline,)
    readonly_fields = ('created_at', 'updated_at')


class CartProductAdminInline(admin.TabularInline):
    model = CartProduct


class CartAdmin(admin.ModelAdmin):
    inlines = (CartProductAdminInline,)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Newsletter)
