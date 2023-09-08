from django.contrib import admin
from .models import Conversation

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'message', 'timestamp')

admin.site.register(Conversation, ConversationAdmin)


