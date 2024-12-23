from django.contrib import admin
from .models import Notes, Tag

class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date')

admin.site.register(Notes, NotesAdmin)
admin.site.register(Tag)