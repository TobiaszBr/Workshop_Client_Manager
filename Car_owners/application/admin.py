from django.contrib import admin
from .models import Owner, Car


class CarInLine(admin.TabularInline):
    model = Car


class OwnerAdmin(admin.ModelAdmin):
    inlines = [CarInLine]


class CarAdmin(admin.ModelAdmin):
    list_display = ("__str__", "owner")
    list_filter = ("owner",)


admin.site.register(Owner, OwnerAdmin)
admin.site.register(Car, CarAdmin)
