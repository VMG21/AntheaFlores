from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from db.models import User

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number' ]
