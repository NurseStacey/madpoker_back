from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import UserModel

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        modela=UserModel
        fields=('email',)