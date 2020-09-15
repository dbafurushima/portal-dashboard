from django.contrib import admin
from .models import Note, Comment, Host, Inventory, Application


@admin.register(Note)
class NoteList(admin.ModelAdmin):
    list_display = ('id', 'subject', 'msg', 'read', 'deleted', 'number_of_comments')
    search_fields = ('subject', 'msg')
    list_filter = ('read', 'deleted')
    list_display_links = ('msg', 'subject')
    list_per_page = 20

    def number_of_comments(self, obj):
        return Comment.objects.filter(note_id=obj.id).count()


@admin.register(Comment)
class CommentList(admin.ModelAdmin):
    list_display = ('id', 'comment_text', 'commented_by', 'updated_at')
    search_fields = ('comment_text',)
    list_filter = ('commented_by',)
    list_display_links = ('comment_text',)
    list_per_page = 20

    def comment_text(self, obj):
        return obj.comment[:40]


@admin.register(Host)
class HostList(admin.ModelAdmin):
    list_display = ('os_name', 'platform', 'ram', 'cores', 'frequency', 'equipment')
    search_fields = ('platform',)
    list_display_links = ('platform',)
    list_per_page = 20


@admin.register(Inventory)
class InventoryList(admin.ModelAdmin):
    list_display = ('id', 'enterprise',)
    search_fields = ('enterprise',)
    list_display_links = ('enterprise',)
    list_per_page = 20


@admin.register(Application)
class ApplicationList(admin.ModelAdmin):
    list_display = ('id', 'name', 'port', 'host')
    search_fields = ('name', 'port')
    list_display_links = ('port',)
    list_per_page = 20
