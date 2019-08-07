from django.contrib import admin
from .models import Post, Comment, Likes

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class LikesInline(admin.TabularInline):
    model = Likes
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, LikesInline]

admin.site.register(Post, PostAdmin)
# admin.site.register(Comment)
# admin.site.register(Likes)
