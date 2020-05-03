from django import template

from blog.models import Comment, ResponseComment, Category, Article

register = template.Library()

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

