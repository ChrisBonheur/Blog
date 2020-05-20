from django import template
from django.core.paginator import Paginator
from math import ceil

from blog.models import ResponseComment
 
register = template.Library()

def create_paginator(list_to_pagine, page):
    paginator = Paginator(list_to_pagine, 10)
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


def limit_table(table, limit):
	#limit liste of a table
	liste = table[:limit]

	return liste

def get_image_by_article(obj, article_id):
	#get images from article
	images = obj.filter(article__id=article_id)

	return images #return a list of images

def get_img_with_indice(table, indice):
	#get image in images list from get_image_by_article
	return table[indice].image.url

register.filter('limit_table', limit_table)
register.filter('paginator', create_paginator)
register.filter('pages_numbr', show_pages_nbr)
register.filter('images_by_article', get_image_by_article)
register.filter('indice', get_img_with_indice)

