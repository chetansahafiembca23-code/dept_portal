from django.contrib import admin
from .models import Event, Activity, Enrollment, EventGallery


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1


class EventGalleryInline(admin.TabularInline):
    model = EventGallery
    extra = 3


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'fee')
    inlines = [ActivityInline, EventGalleryInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'activity', 'payment_status', 'enrolled_at')
    list_filter = ('event', 'payment_status', 'activity')
    search_fields = ('user__username', 'user__roll_number', 'transaction_id')
    readonly_fields = ('enrolled_at',)


admin.site.register(Activity)