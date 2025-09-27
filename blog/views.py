from django.shortcuts import render , HttpResponse , redirect
from .models import Blog , Category, SubCategory
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm , SubCategoryForm

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


from .forms import BlogForm

# Create a new blog
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user:all-blogs')
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'Create Blog'})

# Edit an existing blog
@login_required
def blog_edit(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('user:all-blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'Edit Blog'})



# Delete a blog
@login_required
def blog_delete(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        blog.delete()
        return redirect('user:all-blogs')  # redirect to the blog list after deletion
    return render(request, 'blog/blog_confirm_delete.html', {'blog': blog})
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



@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:all-categories')
    else:
        form = CategoryForm()
    return render(request, 'blog/category_form.html', {'form': form, 'title': 'Create Category'})


@login_required
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('user:all-categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def category_delete(request , id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('user:all-categories')
    


#subcategories
@login_required
def subcategory_create(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:all-subcategories')
    else:
        form = SubCategoryForm()
    return render(request, 'blog/subcategory_form.html', {'form': form, 'title': 'Create Category'})


@login_required
def subcategory_edit(request, id):
    subcategory = get_object_or_404(SubCategory, id=id)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('user:all-categories')
    else:
        form = SubCategoryForm(instance=subcategory)
    return render(request, 'blog/subcategory_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def subcategory_delete(request , id):
    category = get_object_or_404(SubCategory, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('user:all-categories')