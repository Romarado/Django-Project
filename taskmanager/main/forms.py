from .models import Racer, Comments
from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RacerForm(ModelForm):
    class Meta:
        model = Racer
        fields = ['name', 'surname', 'abilities']
        #fields = '__all__'
        # widgets = {
        #         'name': TextInput(attrs={
        #             'class': 'form-control',
        #             'placeholder': 'Введите имя'
        #         }),
        #     'surname': TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Введите фамилию'
        #     }),
        #     'abilities': Textarea(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Введите ваши умения',
        #         'style': 'max-height: 250px'
        #     })
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин'
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            })
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['style'] = 'height: 100px'
