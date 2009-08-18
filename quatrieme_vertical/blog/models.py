from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    
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
    image = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    content = models.CharField(max_length=1000)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content
    
class ResponseComment(models.Model):
    content = models.CharField(max_length=1000)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
        