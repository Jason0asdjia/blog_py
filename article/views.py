from django.shortcuts import render
from django.http import HttpResponse

from .models import ArticlePost
# Create your views here.

#读取所有文章
def article_list(request):
    articles = ArticlePost.objects.all()

    #封装成传递给templates 的对象
    context = {'articles' : articles}

    #render渲染，进一步封装，返回context对象，通过浏览器呈现
    return render(request, 'article/list.html', context)

#查看文章详情
def article_detail(request, id):
    #通过id读取文章
    article = ArticlePost.objects.get(id=id)

    #封装
    context = {'article': article}
    #模板渲染，返回给浏览器
    return render(request, 'article/detail.html', context)
