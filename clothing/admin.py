from django.contrib import admin
from .models import Genre, Clothes, User, Clothes_rating


# Register your models here.
# admin.site.register(Genre)
admin.site.register(Clothes)
admin.site.register(User)
admin.site.register(Clothes_rating)