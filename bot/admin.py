from django.contrib import admin
from .models import Conversation, Student, UserProfile

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'message', 'timestamp')

admin.site.register(Conversation, ConversationAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'admission_number', 'fee_balance', 'name')
    list_filter = ('fee_balance',)
    search_fields = ('email', 'admission_number', 'name')

admin.site.register(Student, StudentAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'admission_number')