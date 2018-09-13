from django.shortcuts import render
from blog.models import Article,Category,Comment
from django.http import Http404, HttpResponse
from django.shortcuts import render,render_to_response,get_object_or_404
import json
from datetime import datetime

# Create your views here.
def Index(request):
    """
    博客首页
    :param request:
    :return:
    """
    article_list = Article.objects.all().order_by('-create_time')[0:5]
    return render(request, 'blog/index.html', {
        "article_list":article_list,
    })

def About(request):
    return render(request, 'blog/about.html')

def Link(request):
    return render(request, 'blog/link.html')

def detail(request, pk):
    article = get_object_or_404(Article, nid=pk)
    article.viewed()
    return render(request, 'blog/detail.html', {"article": article})

def comment(request, pk):
    comment_user = request.POST.get('comment_name')
    comment_body = request.POST.get('comment_body')
    if comment_body and comment_user:
        if '<script>' in comment_body or '<script>' in comment_user:
            return HttpResponse(json.dumps({'result': 'fail', 'msg': '防止XSS'}))
        else:
            Comment.objects.create(article_id=pk,
                                   user=comment_user,
                                   content=comment_body)
            return HttpResponse(json.dumps({'result': 'successfully','msg':'添加成功'}))
    else:
        return HttpResponse(json.dumps({'result': 'fail', 'msg': '添加失败'}))

def get_comment(request, pk):
    article_list = get_object_or_404(Article, nid=pk)
    comments = article_list.comment_set.all()
    html = ''
    for i in comments:
        time_str = str(i.create_time).split('.')[0]
        time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        create_time = time.strftime('%Y-%m-%d %H:%M')
        ele = '<div class="cont-ur"><span class="dat">'+create_time+'</span><span class="nam">'+i.user+'说：</span></div><div class="cont-tx"><p>'+i.content+'</p></div>'
        html += ele
    return HttpResponse(json.dumps({'answer': html}))

def Articles(request, pk):
    """
    博客列表页面
    :param request:
    :param pk:
    :return:
    """
    pk = int(pk)
    if pk:
        category_object = get_object_or_404(Category, nid=pk)
        category = category_object.title
        article_list = Article.objects.filter(category_id=pk)
    else:
        # pk为0时表示全部
        article_list = Article.objects.all()  # 获取全部文章
        category = ''
    return render(request, 'blog/articles.html', {"article_list": article_list,
                                                  "category": category,
                                                  })


def archive(request):
    article_list = Article.objects.order_by('-create_time')
    return render(request, 'blog/archive.html', {"article_list": article_list})


def tag(request,name):
    article_list = Article.objects.filter(tags__title=name)
    return render(request, 'blog/tag.html', {"article_list": article_list,
                                             "tag": name})

def search(request):
    key = request.GET['key']
    article_list = Article.objects.filter(title__icontains=key)
    return render(request, 'blog/search.html',
                  {"article_list": article_list, "key": key})

def page_not_found(request):
    return render_to_response('404.html')
