from django.test import TestCase
from django.urls import reverse
from .models import Article, Category, Comment, ResponseComment, Utilisateur, Image
# Create your tests here.

# Index page
class IndexPageTestCase(TestCase):
	def test_index_page(self):
		Category.objects.create(name="la course")
		category = Category.objects.get(name="la course")
		article = Article.objects.create(title="Arrive vite",content="Malgré lui",category=category)
		response = self.client.get(reverse('index'))
		#test that index return 200
		self.assertEqual(response.status_code, 200)
	

#Read Article
class ReadArticle(TestCase):

	def setUp(self):
		Category.objects.create(name="la course")
		category = Category.objects.get(name="la course")
		Article.objects.create(title="Arrive vite",content="Malgré lui",category=category)	
		self.article = Article.objects.get(title="Arrive vite")
		self.user = Utilisateur.objects.create(username="bonheur",email="bonheur@gmail.com",password="123456",gender="homme")
		self.get_user = Utilisateur.objects.get(username="bonheur")
		Comment.objects.create(content="Blabla",utilisateur=self.user,article=self.article)
		self.comment = Comment.objects.get(article=self.article)
	#test that read article return a 200 if article_id exist
	def test_read_article_return_200(self):
		article_id = self.article.id
		response = self.client.get(reverse('blog:single', args=(article_id,)))
		
		self.assertEqual(response.status_code, 200)
	
	#test that read article return a 404 if article_id not exist
	def test_read_article_return_404(self):
		article_id = self.article.id + 1
		response = self.client.get(reverse('blog:single', args=(article_id,)))

		self.assertEqual(response.status_code, 404)
	
	#if request
	def test_comment_belong_user_and_article(self):
		#verification if comment_user i belong to user
		self.assertEqual(self.comment.utilisateur, self.user)
		#verification if comment_article is belong to article
		self.assertEqual(self.comment.article, self.article)

	def test_comment_has_been_added(self):
		old_comment = Comment.objects.all().count()
		new_comment = Comment.objects.create(content="On arrive ...",utilisateur=self.user,article=self.article)
		new_comment = Comment.objects.all().count()
		
		self.assertEqual(old_comment, new_comment - 1)	