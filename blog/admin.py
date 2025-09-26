from django.contrib import admin
from .models import Blog , Category, SubCategory

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at", "published")
    search_fields = ("title", "author")  # author is a CharField
    list_filter = ("published", "created_at", "updated_at")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}  # auto-fill slug from title
    readonly_fields = ("created_at", "updated_at")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description" ,"slug")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "description")
    search_fields = ("name", "category__name")  # search by subcategory name and category name
    list_filter = ("category",)
    ordering = ("name",)
