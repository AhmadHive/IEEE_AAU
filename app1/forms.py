from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, Post,Socity


class CreateOfficerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    academic_year = forms.ChoiceField(choices=User.Academic_Year, required=True)
    major = forms.CharField(required=True, max_length=100)
    socity = forms.ModelChoiceField(queryset=Socity.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'academic_year', 'major', 'socity', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False 
        if commit:
            user.save()
        return user


class Login_Form(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            
            if self.user_cache is None:
                raise forms.ValidationError("Email or password is incorrect")
            elif not self.user_cache.is_active:
                
                raise forms.ValidationError(
                    "Your account is not active yet. Please contact the administrator to activate your account."
                )
        return self.cleaned_data
            

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'img']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'content': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
            'img': forms.FileInput(attrs={'class': 'input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].required = False