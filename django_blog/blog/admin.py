from django.contrib import admin

# Register your models here.
from blog import models

admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Comment)

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_time'
    list_display = ('title', 'category', 'user', 'create_time', 'view')
    list_filter = ('category', 'user')
    filter_horizontal = ('tags',)
