from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import markdown

from .forms import ArticlePostForm
from .models import ArticlePost
# Create your views here.

#读取所有文章
def article_list(request):
    articles = ArticlePost.objects.all()

    #将context使用articles模板进行加载
    context = {'articles' : articles}

    #render渲染，进一步封装，返回context对象，通过浏览器呈现
    return render(request, 'article/list.html', context)

#查看文章详情
def article_detail(request, id):
    #通过id读取文章
    article = ArticlePost.objects.get(id=id)

    # #封装
    # context = {'article': article}
    # #模板渲染，返回给浏览器
    # return render(request, 'article/detail.html', context)

    #使用markdown语法渲染成html样式
    article.body = markdown.markdown(article.body.replace("r/n/", "/n"),
                                                                                    extensions=[
                                                                                        'markdown.extensions.extra',  #缩写，表格等扩展
                                                                                        'markdown.extensions.codehilite',#高亮插件
                                                                                        'markdown.extensions.toc', #自动生成目录
                                                                                    ]
    )

    context = {'article' : article}
    return render(request, 'article/detail.html', context)

#提交文章的页面
def article_create(request):
    #如果用户提交数据
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        #判断数据是否满足要求
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            #创立新的id作者,默认为id=1的作者
            new_article.author = User.objects.get(id=1)
            #存入数据库
            new_article.save()
            #save后返回文章列表页面
            return redirect("article:article_list")
    
        #如果数据不符合要求
        else:
            return HttpResponse("表单内容非法，清重新填写！")

    #如果用户请求获取数据GET
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form' : article_post_form}
        return render(request, 'article/create.html', context)

#删除文章页面
def article_delete(request, id):
    #根据id删除文章
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")