from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from random import choice
from PIL import Image as Img

from .models import Article, Category, Comment, ResponseComment, Utilisateur, Image
from .forms import CommentForm
 
#Get Element on database
articles = Article.objects.all()
comments = Comment.objects.all()
categories = Category.objects.all()
images = Image.objects.all()
responses = ResponseComment.objects.all()

def get_random_articles(nbr_of_article, list_aricles):
    # this function a random list of articles with their comments count in dict
    random_post_comment = {}
    for i in range(nbr_of_article):
        article = choice(list_aricles)
        comment_count = comments.filter(article__title=article.title).count()
        random_post_comment[article] = comment_count
    
    return random_post_comment;

def create_paginator(request, list_to_pagine, articles_by_page):
    #Create a paginator list 
    paginator = Paginator(list_to_pagine, articles_by_page)
    page = request.GET.get('page')
    default_page = 1

    try:
        paginator.page(page)
    except PageNotAnInteger:
        list_pagined = paginator.page(default_page)
    except EmptyPage:
        list_pagined = paginator.page(default_page)
    else:
        list_pagined = paginator.page(page)

    return list_pagined

def index(request):
    last_article = Article.objects.last()
    articles = Article.objects.exclude(pk=last_article.id).order_by("-date_create")

    context = {
        "block_title": "Dernier article publié",
        "articles": articles,
        "articles_pagined": create_paginator(request, articles, 2),
        "comments": comments,
        "last_article": last_article,
        "categories": categories,
        "images": images,
        "random_posts": get_random_articles(2, articles),
    }
    
    return render(request, 'blog/index.html', context)

def read_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    response = request.GET.get('response')

    comment = []
    if not response:#verifie if response not exist
        response = "hide"
    elif response != "hide":
        comment = Comment.objects.get(pk=response)#get unique comment
    
    form = CommentForm()
    
    context = {
        "block_title": "Article",
        "comments": comments,
        "comment": comment,
        "article": article,
        "response": response,
        "articles": articles,
        "categories": categories,
        "ResponseComment": responses,
        "form": form
    }

    if request.method == "POST":
        if CommentForm(request.POST).is_valid():
            email = request.POST.get('email')
            name = request.POST.get('name')
            message = request.POST.get('message')
            utilisateur = Utilisateur.objects.filter(email=email)
            response = request.POST.get('response')
        
            if not utilisateur:
                utilisateur = Utilisateur.objects.create(
                    username=name,
                    email=email,
                    password=1234,
                    gender="Gender"
                    )
            else:
                utilisateur = Utilisateur.objects.get(email=email)
            
            #verification if response from comment is hide or id for comment
            if response == "hide":
                comment = Comment.objects.create(
                    content=message,
                    utilisateur=utilisateur,
                    article=article
                    )
            else:
                try:
                    comment = Comment.objects.get(pk=response)
                except Exception as e:
                    raise e
                else:
                    comment_answer = ResponseComment.objects.create(
                        content=message,
                        utilisateur=utilisateur,
                        comment=comment
                        )

            return redirect('/blog/{}/?response={}#comments'.format(article_id, response))
            
        else:
            context['errors'] = form.errors.items()


    return render(request, 'blog/blog-single.html', context)

def about(request):
    """This function customise the about.html page"""
    context = {
        "block_title": "A PROPOS",
        "articles": articles,
        "comments": comments,
        "categories": categories,
        "images": images
    }
    return render(request, 'blog/about.html', context)

def contact(request):
    
    context = {
        "block_title": "Contact",
        "articles": articles,
        "comments": comments,
        "categories": categories,
        "images": images
    }
    return render(request, 'blog/contact.html', context)

def search(request):
    query = request.GET.get('query')
    query = str(query)
    title = 'Résultat pour la recherche "{}"'.format(query)
    
    if not query:
        articles = articles
    else:
        articles = Article.objects.filter(title__icontains=query)
        if not articles:
            articles = Article.objects.filter(category__name__icontains=query)
            if not articles:
                title = 'Aucun résultat pour la recherche "{}"'.format(query)
    page = get_page(request)

    context = {
        "block_title": title,
        "articles": articles,
        "comments": comments,
        "title": title,
        "random_posts": get_random_articles(4, Article.articles),
        "categories": categories,
        "query": query,
        "page": page,
        "images": images
    }
    
    return render(request, 'blog/search.html', context)


