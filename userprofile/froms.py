from django import forms
from django.contrib.auth.models import User

#登陆表单
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

#用户注册
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    #验证密码
    def clean_repassword(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试！")
