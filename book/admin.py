from django.contrib import admin
from .models import Book, Review, LikeForBook

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(LikeForBook)