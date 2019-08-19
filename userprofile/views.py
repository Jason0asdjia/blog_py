from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile

# Create your views here.

#用户登陆界面
def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)

        if user_login_form.is_valid():
            #清洗合法数据
            data= user_login_form.cleaned_data
            #检验账号密码是否存在
            #如果都符合返回此账号
            user = authenticate(username=data['username'], password=data['password'])

            if user:
                #将用户保存在session中，实现登陆
                login(request, user)
                return redirect("article:article_list")
            
            else:
                return HttpResponse("账号密码输入错误，清重新输入！")
            
        else:
            return HttpResponse("账号密码输入不合法，清重新输入！")
        
    elif request.method =="GET":
        user_login_form = UserLoginForm()
        context = {'form' : user_login_form}
        return render(request, 'userprofile/login.html', context)

    else:
        return HttpResponse("非法请求！！")
        
#用户登出
def user_logout(request):
    logout(request)
    return redirect("article:article_list")

#用户注册
def user_register(request):
    if request.method == "POST":
        user_register_form = UserRegisterForm(data=request.POST)

        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)

            new_user.set_password(user_register_form.cleaned_data["password"])
            new_user.save()

            login(request, new_user)
            return redirect("article:article_list")

        else:
            return HttpResponse("注册信息输入有误，清重新输入！")
    
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form':user_register_form}
        return render (request, 'userprofile/register.html', context)
        
    else:
        return HttpResponse("非法请求！！")

#删除用户
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        #退出登陆并删除用户
        logout(request)
        user.delete()
        return redirect("article:article_list")
        # return HttpResponse("chengg")

    else:
        return HttpResponse("权限不足！！")

#编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    #因为信号接收器的原因，无法动态获取
    # profile = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == "POST":
        if request.user != user:
            return HttpResponse("权限不足！！")
        # profile_form = ProfileForm(data=request.POST)
        # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            # print(profile_cd)
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()

            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("信息有误，清重新填写！")
    elif request.method == "GET":
        # profile_form = ProfileForm()  //bootstrap已经写好表单，不需要这个对象
        context = {'profile':profile, 'user':user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请求非法！")

