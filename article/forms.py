from django import forms

from .models import ArticlePost

#文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #数据来源
        model = ArticlePost
        #定义表单包含的字段
        fields = ('title', 'body')