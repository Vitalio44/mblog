from django.contrib import admin
from posts.models import UserProfile
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "updated", "timestamp", "keywords", "description"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = Post

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)