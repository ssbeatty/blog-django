import re
import markdown
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def custom_markdown(value):
    content = mark_safe(markdown.markdown(value, extensions=['markdown.extensions.fenced_code',
                                                             'markdown.extensions.codehilite',
                                                             'markdown.extensions.tables'],
                                          safe_mode=True, enable_attributes=False))
    return content



@register.filter
def slice_list(value, index):
    return value[index]


@register.simple_tag(takes_context=True)
def paginate(context, object_list, page_count):
    context['count'] = object_list.count
    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page')

    try:
        object_list = paginator.page(page)
        context['current_page'] = int(page)

    except PageNotAnInteger:
        object_list = paginator.page(1)
        context['current_page'] = 1
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages

    context['article_list'] = object_list
    context['last_page'] = paginator.num_pages
    context['first_page'] = 1
    return ''  # 必须加这个，否则首页会显示个None

@register.filter
def getTag(value):
    """
    展示一个tag
    :param value:
    :return:
    """
    tag = ''
    for each in value:
        if each.get('title'):
            tag = each.get("title")
            break
    return tag


@register.filter
def tag2string(value):
    """
    将Tag转换成string >'python,爬虫'
    :param value:
    :return:
    """
    return ','.join([each.get('title', '') for each in value])



if __name__ == '__main__':
    pass
