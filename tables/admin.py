from django.contrib import admin
from .models import Group,Schedule,Faculty
# Register your models here.

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["group_key","date"]
    class Meta:
        model = Schedule

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0

class GroupAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]

admin.site.register(Faculty)
admin.site.register(Group, GroupAdmin)
admin.site.register(Schedule, ScheduleAdmin)