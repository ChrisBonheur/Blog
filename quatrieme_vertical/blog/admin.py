from django.contrib import admin

from .models import Utilisateur, Article, Comment, ResponseComment, Category, Image

admin.site.register(Utilisateur)
admin.site.register(Article)
admin.site.register(ResponseComment)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Image)


