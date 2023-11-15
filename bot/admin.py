from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Conversation, Student, UserProfile

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('message', 'timestamp')

admin.site.register(Conversation, ConversationAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'admission_number', 'fee_balance', 'name')
    list_filter = ('fee_balance',)
    search_fields = ('email', 'admission_number', 'name')

admin.site.register(Student, StudentAdmin)

class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ['username', 'email', 'is_staff']

admin.site.register(UserProfile, UserProfileAdmin)