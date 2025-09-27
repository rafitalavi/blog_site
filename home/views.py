from django.shortcuts import render , HttpResponse , redirect
from django.contrib import messages
from .forms import ContactForm , WebsettingForm
from .models import Banner , Websetting
from blog.models import Blog
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    banner = Banner.objects.all()
    blogs = Blog.objects.all()[:4]
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # redirect to same page or a success page
        else:
            messages.error(request, "There was an error. Please correct the form and try again.")
    else:
        form = ContactForm()

    context = {'banner': banner,
               'blogs' : blogs,
               'form':form}
 
    return render(request, 'home/home.html', context)




def about(request):
    return render(request, 'home/about.html')
def contact(request):
    websetting = Websetting.objects.first()  # get the first (or only) websetting

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # redirect to same page or a success page
        else:
            messages.error(request, "There was an error. Please correct the form and try again.")
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'websetting': websetting
    }
    return render(request, 'home/contact.html', context)
# home/context_processors.py


# home/context_processors.py



