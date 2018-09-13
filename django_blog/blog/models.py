from django.db import models
from mdeditor.fields import MDTextField
# Create your models here.


class Category(models.Model):
    """
    个人博客文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)  # 分类标题

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    标签
    """
    title = models.CharField(max_length=32)  # 标签名

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    文章
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="文章标题")  # 文章标题
    desc = models.CharField(max_length=255, verbose_name='文章描述')  # 文章描述
    create_time = models.DateTimeField()  # 创建时间  --> datetime()
    view = models.BigIntegerField(verbose_name='阅读数' ,default=0)  # 阅读数
    # 评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    picture = models.CharField(max_length=200,verbose_name='展示图片地址')  # 标题图片地址
    content = MDTextField(verbose_name='文章正文')

    category = models.ForeignKey(to="Category", to_field="nid", null=True)
    user = models.CharField(max_length=25, default='admin')
    tags = models.ManyToManyField(Tag)
    def viewed(self):
        """
        增加阅读数
        :return:
        """
        self.view += 1
        self.save(update_fields=['view'])



    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']



class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    user = models.CharField(max_length=25)
    content = models.CharField(max_length=255)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, blank=True)  # blank=True 在django admin里面可以不填

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-create_time']
        verbose_name = "评论"
        verbose_name_plural = verbose_name

