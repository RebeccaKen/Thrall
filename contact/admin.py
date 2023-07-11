from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'date', 'rating')
    list_filter = ('date', 'rating')
    search_fields = ('name', 'email', 'comments')
    actions = ['approve_feedback']

    def approve_Comments(self, request, queryset):
        queryset.update(approved=True)

