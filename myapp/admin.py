from django.contrib import admin
from myapp.models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
class BlogAdmin(admin.ModelAdmin):
    list_display=[
        'user','category','title','blog_slug','image'
    ]
admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogSubImg)
admin.site.register(CommentUser)
admin.site.register(Likes)