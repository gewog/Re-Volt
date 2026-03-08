from django.contrib import admin
from .models import BatterySubmission


@admin.register(BatterySubmission)
class BatterySubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'count', 'city', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
