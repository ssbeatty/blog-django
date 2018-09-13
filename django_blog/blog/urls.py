from blog import views
from django.conf.urls import url

urlpatterns = [
    url(r'^index/$', views.Index, name='index'),
    url(r'^about/$', views.About, name='about'),
    url(r'^link/$', views.Link, name='link'),
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^comment/(?P<pk>\d+)/$', views.comment, name='comment'),
    url(r'^get_comment/(?P<pk>\d+)/$', views.get_comment, name='get_comment'),
    url(r'^article/(?P<pk>\d+)/$', views.Articles, name='article'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^tag/(?P<name>.*?)/$', views.tag, name='tag'),
    url(r'^search/$', views.search, name='search'),

]
