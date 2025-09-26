from django.shortcuts import render , HttpResponse

# Create your views here.

def blog_home(request):
    return render(request, 'blog/bloghome.html')
def blog_post(request, slug):
    return render(request, 'blog/blogpost.html', {'slug': slug})