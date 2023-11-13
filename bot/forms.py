from django import forms
from django.contrib.auth.forms import UserCreationForm
from bot.models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=150, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')

    class Meta(UserCreationForm.Meta):
        model = UserProfile  
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'password_too_short': "Your password must contain at least 8 characters.",
        'password_common': "Your password can’t be a commonly used password.",
        'password_entirely_numeric': "Your password can’t be entirely numeric.",
        'password_similar': "Your password can’t be too similar to your other personal information.",
    }
