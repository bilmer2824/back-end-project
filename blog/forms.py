from django import forms
from .models import Article
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import User, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'photo',
            'is_published',
            'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomi'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Matni"
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Foydalanuvchi ismi",
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control'
                               }))
    password = forms.CharField(label="Parol",
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control'
                               }))



class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text="Maksimal uzunlik 150",
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'form3Example1c'
                                   # 'placeholder': "Foydalanuvchi ismi"
                               }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': "form3Example4c"
        # 'placeholder': 'Parol'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': "form3Example4cd"
        # 'placeholder': 'Parolni takrorlang'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': "form3Example3c"
        # 'placeholder': 'Email'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Sizning comentariyangizni matni..."
            })
        }