from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    prepopulated_fields = {'slug': ('name',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'get_category', 'create_date', 'get_tag', 'is_paid', 'user')
    prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('user',)

    def get_category(self, obj):
        categories = [category.name for category in obj.category.all()]
        return ", ".join(categories)
    get_category.short_description = 'category'

    def get_tag(self, obj):
        tags = [tag.name for tag in obj.tags.all()]
        return ", ".join(tags)
    get_tag.short_description = 'tags'

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'user', 'parent', 'approved', 'create_date')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Tag, TagAdmin)