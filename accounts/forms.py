from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm

from accounts.models import User


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True  # class Meta - fields에 접근, 필수 요소로 만들겠다.
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')  # 현재 사용자가 입력한 이메일을 깔끔한 상태인 cleaned_data에 넣어준다
        if email:
            qs = User.objects.filter(email=email)  # User.objects의 email에 현재 입력한 이메일을 넣어준다
            if qs.exists():
                raise forms.ValidationError('이미 등록된 이메일 입니다')  # 존재한다면 여기서 if문 끝나므로 에러상태에서 머무를 것
        return email


# 나중에 인스타그램에서도 사용할것
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'phone_number', 'bio']


class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        password2 = super().clean_new_password2()
        if old_password == password2:
            raise forms.ValidationError('기존과 다른 비밀번호를 입력해주세요')
        return password2

