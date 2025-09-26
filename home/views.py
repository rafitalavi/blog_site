from django.shortcuts import render , HttpResponse , redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Banner
# Create your views here.
def home(request):
    banner = Banner.objects.all()
    context = {'banner': banner}
 
    return render(request, 'home/home.html', context)




def about(request):
    return render(request, 'home/about.html')
def contact(request):
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
    return render(request, 'home/contact.html',{'form': form})