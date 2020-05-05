from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from random import choice

from .models import Article, Category, Comment, ResponseComment, Utilisateur
from .forms import CommentForm

def searching_article(indice_to_find):
    result_search = []#list of search result
    # searching articles by title
    articles_by_title = Article.objects.filter(title__icontains=indice_to_find)
    result_search += (articles_by_title)#adding result to resultsearch
    #if not result we continues searching with article by category
    if not articles_by_title:
        #searching by category
        categories = Category.objects.filter(name__icontains=indice_to_find)
        # loop to find all articles with categories name found
        for category in categories:
            articles_by_category = Article.objects.filter(category=category)
            result_search += articles_by_category#adding result to resultsearch
    
    return result_search    

def get_random_articles(nbr_of_article, list_aricles):
    # this function a random list of articles with their comments count in dict
    random_post_comment = {}
    for i in range(nbr_of_article):
        article = choice(list_aricles)
        comment_count = Comment.objects.filter(article__title=article.title).count()
        random_post_comment[article] = comment_count
    
    return random_post_comment;

def get_page(request):
    default_page = 1
    page = request.GET.get('page')

    if page:
        try:
            page = int(page)
        except PageNotAnInteger:
            page = default_page
        except EmptyPage:
            page = default_page
    else:
        page = default_page

    return page

def articles_comment_count(request, nbr_article_by_page, filter_name=""):
    """This function create a list with articles by page and return
    two element variable must be like a, b = articles_comment_count
    """
    #verifictaion if filter exist to return articles with filter or no
    if filter_name == "":
        all_articles_list = Article.objects.all().order_by("-date_create")
    else:
        all_articles_list = searching_article(filter_name)
               
    #cretaing paginator with all_articles
    all_articles = create_paginator(request, all_articles_list, nbr_article_by_page)
    #creating of dictionnary (article and their comment count)    
    articles_comments = {} #this for all article and their comment count
    for article in all_articles:
        #this loop add to dict article_comment the key and value(article and comment count)
        comments = Comment.objects.filter(article__title=article.title)
        responses_comment = ResponseComment.objects.filter(comment__article=article)
        #sum of comment and their response to get total comments_count()
        comments_count = comments.count() + responses_comment.count()

        articles_comments[article] = comments_count
    
    return all_articles, articles_comments

def categories_articles_count():
    """This function return table of categories and dict(categories with their 
    count articles)"""
    categories = Category.objects.all()
    #creating of dictionnary for categories with their articles count
    categories_articles_count = {}
    for category in  categories:
        #This loop add to dict categories_articles_count categories and their count article
        article_count = Article.objects.filter(category__name=category.name).count()
        categories_articles_count[category] = article_count
    
    return categories, categories_articles_count

def get_articles_limit(limit_number):
    """this function get articles with limited_number"""
    last_article = Article.objects.last()
    all_articles_limit = Article.objects.exclude(pk=last_article.id)[:limit_number]
    #creating of dictionnary (article and their comment count)
    articles_comments_limit = {} # this for article limit  and their comment count
    for article in all_articles_limit:
        #this loop add to dict article_comment the key and value(article and comment count)
        comment_count = Comment.objects.filter(article__title=article.title).count()
        articles_comments_limit[article] = comment_count   
    
    return articles_comments_limit    

def get_comments_response(request, article_title, nbr_article_by_page, comment_id=""):
    """This function get comment and their response and return in paginator a 
    dict comment: responsesComments and comments to create a button to naviguate on pages""" 
    comments = Comment.objects.filter(article__title=article_title)
    #we try to verif if we want just to get one comment
    if comment_id != "":
        comments = Comment.objects.filter(pk=comment_id)

    comments = create_paginator(request, comments, nbr_article_by_page)
    comments_responses = {}
    for comment in comments:
        responses_comment = ResponseComment.objects.filter(comment__id=comment.id)
        # responses_comment = create_paginator(request, responses_comment, 8)
        comments_responses[comment] = responses_comment

    return comments, comments_responses 

def index(request):
    last_article = Article.objects.last()         
    articles = Article.objects.all()
    
    page = get_page(request)

    context = {
        "block_title": "Dernier article publié",
        "articles": articles,
        "comments": Comment.objects.all(),
        "last_article": last_article,
        "categories": Category.objects.all(),
        "random_posts": get_random_articles(2, articles),
        "page": page
    }
    
    return render(request, 'blog/index.html', context)

def read_article(request, article_id):
    article = Article.objects.get(pk=article_id)

    response = request.GET.get('response')
    if not response:
        response = "hide"

    form = CommentForm()

    context = {
        "block_title": "Article",
        "comments": Comment.objects.all(),
        "article": article,
        "response": response,
        "articles": Article.objects.all(),
        "categories": Category.objects.all(),
        "ResponseComment": ResponseComment.objects.all(),
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
        "articles": Article.objects.all(),
        "comments": Comment.objects.all(),
        "categories": Category.objects.all(),
    }
    return render(request, 'blog/about.html', context)

def contact(request):
    categories, categories_articles = categories_articles_count()
    context = {
        "block_title": "Contact",
        "articles": Article.objects.all(),
        "comments": Comment.objects.all(),
        "categories": Category.objects.all()
    }
    return render(request, 'blog/contact.html', context)

def search(request):
    query = request.GET.get('query')
    query = str(query)
    title = 'Résultat pour la recherche "{}"'.format(query)
    
    if not query:
        articles = Article.objects.all()
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
        "comments": Comment.objects.all(),
        "title": title,
        "random_posts": get_random_articles(4, Article.objects.all()),
        "categories": Category.objects.all(),
        "query": query,
        "page": page
    }
    
    return render(request, 'blog/search.html', context)


