from django.contrib import admin
from .models import ChatConversation


class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','prompt', 'created_at')
    list_filter = ('user',)
    search_fields = ('user',)


admin.site.register(ChatConversation, ChatConversationAdmin)
