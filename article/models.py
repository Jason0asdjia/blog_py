from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone

# 博客文章数据模型
#使用ORM操作数据
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 用于保存较短的字符串
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 创建时间 default=timezone.now 在创建数据时将默认写入当前的时间
    created_time = models.DateTimeField(default=timezone.now)

    # 更新时间。参数 auto_now=True 数据更新时自动写入当前时间
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        ordering = ('-created_time',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        #需要返回数据时， 将文章标题返回
        return self.title