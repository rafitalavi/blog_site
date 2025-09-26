from django.shortcuts import render , HttpResponse
from .models import Blog , Category, SubCategory
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


# Create your views here.

def blog_home(request):
    blogs = Blog.objects.filter(published=True)

    # Filters
    category_slug = request.GET.get('category')
    subcategory_slug = request.GET.get('subcategory')
    
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)
    if subcategory_slug:
        blogs = blogs.filter(subcategory__slug=subcategory_slug)

    # Pagination
    paginator = Paginator(blogs, 12)  # 12 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    context = {
        'blogs': page_obj,
        'categories': categories,
        'subcategories': subcategories,
        'page_obj': page_obj
    }
    return render(request, 'blog/bloghome.html', context)

def blog_post(request, slug):
    blog = get_object_or_404(Blog, slug=slug, published=True)

    # Get related posts: same subcategory, exclude current, limit 4
    related_posts = Blog.objects.filter(
        subcategory=blog.subcategory,  # make sure you have a ForeignKey in Blog
        published=True
    ).exclude(id=blog.id)[:4]

    context = {
        'blog': blog,
        'related_posts': related_posts,}
    return render(request, 'blog/blogpost.html', context)

def search_blogs(request):
    query = request.GET.get('q')
    blogs = Blog.objects.filter(published=True)
    if query:
        blogs = blogs.filter(title__icontains=query)  # Simple case-insensitive search

    paginator = Paginator(blogs, 12)  # 12 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'blog/bloghome.html', context)       