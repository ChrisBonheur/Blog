from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name="home"),
    url(r'^about/$', views.about, name="about"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^(?P<article_id>[0-9]+)/$', views.single_article, name="single"),
    url(r'^search/$', views.search, name="search"),
]

app_name = "blog"

