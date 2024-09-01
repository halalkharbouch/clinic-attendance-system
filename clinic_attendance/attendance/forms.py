from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class StaffRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    department = forms.CharField(max_length=100, required=True)
    staff_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "department", "staff_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_class = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': self.field_class})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.department = self.cleaned_data['department']
        user.staff_number = self.cleaned_data['staff_number']
        user.is_staff_member = True
        user.set_password('12345678')  # Automatically set a random password
        if commit:
            user.save()
        return user
