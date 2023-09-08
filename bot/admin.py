from django.contrib import admin
from .models import Conversation, Student

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'message', 'timestamp')

admin.site.register(Conversation, ConversationAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'admission_number', 'fee_balance', 'name')
    list_filter = ('fee_balance',)
    search_fields = ('email', 'admission_number', 'name')

admin.site.register(Student, StudentAdmin)