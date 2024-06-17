from django.contrib import admin
from .models import Website, Category, EntryCount, websiteFlagCount, validationWithTime, validationForLowStock, validationForActivityNotification

@admin.register(EntryCount)
class EntryCountAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'count']

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['webName', 'baseURL', 'contains', 'lastFlagAt']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['patternName', 'count']

@admin.register(websiteFlagCount)
class websiteFlagCountAdmin(admin.ModelAdmin):
    list_display = ['website', 'year', 'month', 'count']

@admin.register(validationWithTime)
class validationWithTimeAdmin(admin.ModelAdmin):
    list_display = ['baseUrl', 'prod_name', 'shown_time', 'init_time']

@admin.register(validationForLowStock)
class validationForLowStockAdmin(admin.ModelAdmin):
    list_display = ['baseUrl', 'prod_name', 'quantity']

@admin.register(validationForActivityNotification)
class validationForActivityNotificationAdmin(admin.ModelAdmin):
    list_display = ['baseUrl', 'prod_name', 'msg', 'timestamp']