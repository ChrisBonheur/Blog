from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from math import ceil

from blog.models import Comment, ResponseComment, Category, Article

register = template.Library()

def create_paginator(list_to_pagine, page):
    paginator = Paginator(list_to_pagine, 2)
    try:
    	list_pagined = paginator.page(page)
    except PageNotAnInteger:
    	list_pagined = paginator.page(1)
    except EmptyPage:
    	list_pagined = paginator.page(1)

    return list_pagined

def show_pages_nbr(list_pagined, elt_by_page):
	pages_numbr = len(list_pagined) / elt_by_page
	pages_numbr = ceil(pages_numbr)
	pages_list = []
	page = 0
	for i in range(pages_numbr):
		page += 1
		pages_list.append(page)

	return pages_list

def get_article_count_by_categories(objArticle, category_id):
	articles = objArticle.filter(category__id=category_id)
	articles_count = articles.count()

	return articles_count

def get_comment_count_by_article(objComment, article_id):
	comments = objComment.filter(article__id=article_id)
	comments_count = comments.count()
	responses_list = []
	for comment in comments:
		responses_count = ResponseComment.objects.filter(comment__id=comment.id)
		if responses_count:
			responses_list.append(responses_count)

	get_obj_count = comments_count + len(responses_list)

	return get_obj_count

def get_response_count_by_comment(objResponse, comment_id):
	get_obj_count = objResponse.filter(comment__id=comment_id).count()
	
	return get_obj_count

def get_response_by_comment(obj, comment_id):
	responses = obj.filter(comment__id=comment_id)

	return responses

def get_comments_by_article(objComment, article_id):
	comments = objComment.filter(article__id=article_id)

	return comments

def get_comment(objComment, comment_id):
	obj = objComment.filter(pk=comment_id)

	return obj

def limit_table(table, limit):
	liste = table[:limit]

	return liste

register.filter('responses_count_filter', get_response_count_by_comment)
register.filter('responses_filter', get_response_by_comment)
register.filter('comments_filter', get_comments_by_article)
register.filter('comments_count_filter', get_comment_count_by_article)
register.filter('article_count_by_category_filter', get_article_count_by_categories)
register.filter('limit_table', limit_table)
register.filter('get_comment', get_comment)
register.filter('paginator', create_paginator)
register.filter('pages_numbr', show_pages_nbr)

