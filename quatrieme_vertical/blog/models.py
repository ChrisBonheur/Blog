from django.db import models
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    
    @property
    def count_art(self):
        """ This function get nombre of article by categories"""
        articles = Article.objects.filter(category__id=self.id) 

        return articles.count()
    
    def __str__(self):
        return self.name

class Utilisateur(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    

class Article(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        comments_count = Comment.objects.filter(article__id=self.id).count()
        
        return comments_count
    
    @property
    def comments(self):
        comments = Comment.objects.filter(article__id=self.id)
        
        return comments

    @property
    def test(self):
        images = Image.objects.all()
        return images
    
class Image(models.Model):
    image = models.ImageField(upload_to='uploads', null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)

    
class Comment(models.Model):
    content = models.CharField(max_length=1000)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.content

    @property
    def response_count(self):
        #get reponses count of a comment
        responses_count = ResponseComment.objects.filter(comment__id=self.id).count()
        
        return responses_count

    @property
    def get_reponses(self):
        responses = ResponseComment.objects.filter(comment__id=self.id)

        return responses
    
    
    
class ResponseComment(models.Model):
    content = models.CharField(max_length=1000)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
        