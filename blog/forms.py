
from .models import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm,  PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('내용',)


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class MyPasswordChangeForm(PasswordChangeForm, SetPasswordForm):
    old_password = forms.Field(label="기존 비밀번호")

    new_password1 = forms.Field(label="새 비밀번호")
    new_password2 = forms.Field(label="새 비밀번호 확인 ")
    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": _(
            "기존 비밀번호가 틀립니다. 다시 입력해주세요"
        )
    }
    error_messages = {
        **SetPasswordForm.error_messages,
        "password_mismatch": _("두 비밀번호가 일치하지 않습니다"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs = {'class': 'form-control'}
