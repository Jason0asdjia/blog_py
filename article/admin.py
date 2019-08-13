from django.contrib import admin
from .models import ArticlePost
# Register your models here.


#将admin与ArticlePost表进行关联
admin.site.register(ArticlePost)