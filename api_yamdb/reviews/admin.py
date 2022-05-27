from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category'
    )
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'score',
        'author',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User)
