from .models import Racer, Comments, Bugurt
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RacerForm(ModelForm):
    class Meta:
        model = Racer
        fields = ['name', 'surname', 'abilities']
        #fields = '__all__'
        widgets = {
                'name': TextInput(attrs={
                    'class': 'form-control input-lg',
                    'placeholder': 'Введите имя',
                    'pattern': '[A-ZА-Я][а-яa-z]{1,}'
                }),
            'surname': TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Введите фамилию',
                'pattern': '[A-ZА-Я][а-яa-z]{1,}',
                'minlength': "3",
                'maxlength':  "18"
            }),
            'abilities': Textarea(attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Введите ваши умения',
                'style': 'max-height: 250px'
            })
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control input-lg'


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control input-lg'
        self.fields['username'].widget.attrs['placeholder'] = 'Введите логин'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'


class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Введите логин'
            }),
            'password': TextInput(attrs={
                'class': 'form-control input-lg',
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
            self.fields[field].widget.attrs['class'] = 'form-control input-lg'
        self.fields['text'].widget.attrs['style'] = 'height: 100px'


class BugurtForm(ModelForm):
    class Meta:
        model = Bugurt
        fields = ['bugurtName', 'bugurtTheme', 'bugurtAsIs']
        #fields = '__all__'
        widgets = {
                'bugurtName': TextInput(attrs={
                    'class': 'form-control input-lg',
                    'placeholder': 'Введите название бугурта',

                }),
            'bugurtTheme': TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Введите тему бугурта',

            }),
            'bugurtAsIs': Textarea(attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Введите ваш бугурт',
                'style': 'max-height: 250px'
            })
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control input-lg'