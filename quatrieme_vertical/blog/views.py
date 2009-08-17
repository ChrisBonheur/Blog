from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime as date

from .models import Article, Category, Comment, ResponseComment, Utilisateur


def index(request):
    last_article = Article.objects.last()
    all_articles = Article.objects.exclude(pk=last_article.id)    
    categories = Category.objects.all()
    context = {
        "articles_limit": all_articles[:3],
        "all_articles": all_articles,
        "last_article": last_article,
        "categories": categories
    }
    return render(request, 'blog/index.html', context)

def single_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    context = {
        "article_date": article.date_create,
        "article_title": article.title,
        "article_content": article.content,
        "article_category": article.category
    }
    return render(request, 'blog/blog-single.html', context)

def about(request):
    context = {
        
    }
    return render(request, 'blog/about.html', context)

def contact(request):
    context = {
        
    }
    return render(request, 'blog/contact.html', context)

def search(request):
    query = request.GET.get('query')
    query = str(query)
    if not query:
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(title=query)
        
        if not articles.exists():
            articles = Article.objects.filter(category=query)
    
    title = "Résultat pour la requête %s".query
    
    context = {
        "articles": articles,
        "title": title
    }
    
    return render(request, 'blog/search.html', context)