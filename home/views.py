from django.shortcuts import render , HttpResponse , redirect
from django.contrib import messages
from .forms import ContactForm , WebsettingForm
from .models import Banner , Websetting
from blog.models import Blog
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm ,BannerForm
from blog.models import  Blog
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
def home(request):
    banner = Banner.objects.all()
    blogs = Blog.objects.all()[:4]
    websetting = Websetting.objects.first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()

            # Email to admin
            send_dynamic_email(
                subject="New Contact Message",
                message=f"From: {contact_instance.name}\nEmail: {contact_instance.email}\nMessage: {contact_instance.message}",
                recipient_list=[websetting.smtp_user]
            )

            # Confirmation email to user
            send_dynamic_email(
                subject="We Received Your Message",
                message=f"Hello {contact_instance.name},\n\nThank you for contacting us! We have received your message and will get back to you shortly.\n\nBest regards,\n{websetting.title}",
                recipient_list=[contact_instance.email]
            )

            messages.success(request, "Your message has been sent successfully! A confirmation email has been sent to you.")
            return redirect('home')
        else:
            messages.error(request, "There was an error. Please correct the form and try again.")
    else:
        form = ContactForm()

    context = {
        'banner': banner,
        'blogs': blogs,
        'form': form,
        'websetting': websetting
    }
    return render(request, 'home/home.html', context)





def about(request):
    return render(request, 'home/about.html')
def contact(request):
    websetting = Websetting.objects.first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()

            # Email to admin
            send_dynamic_email(
                subject="New Contact Message",
                message=f"From: {contact_instance.name}\nEmail: {contact_instance.email}\nMessage: {contact_instance.message}",
                recipient_list=[websetting.smtp_user]
            )

            # Confirmation email to user
            send_dynamic_email(
                subject="We Received Your Message",
                message=f"Hello {contact_instance.name},\n\nThank you for contacting us! We have received your message and will get back to you shortly.\n\nBest regards,\n{websetting.title}",
                recipient_list=[contact_instance.email]
            )

            messages.success(request, "Your message has been sent successfully! A confirmation email has been sent to you.")
            return redirect('contact')
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

@login_required
def banner_create(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user:all_banner')
    else:
        form = BannerForm()
    return render(request, 'home/banner_form.html', {'form': form, 'title': 'Create Banner'})
@login_required
def banner_edit(request, id):
    banner = get_object_or_404(Banner, id=id)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('user:all_banner')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'home/banner_form.html', {'form': form, 'title': 'Edit Banner'})
@login_required
def banner_delete(request, id):
    banner = get_object_or_404(Banner, id=id)
    if request.method == 'POST':
        banner.delete()
        return redirect('user:all_banner')  # redirect to the blog list after deletion

def send_dynamic_email(subject, message, recipient_list):
    websetting = Websetting.objects.first()  # get your settings

    # Determine whether to use SSL or TLS
    use_ssl = websetting.smtp_use_ssl
    use_tls = websetting.smtp_use_tls

    try:
        connection = get_connection(
            host=websetting.smtp_host,
            port=websetting.smtp_port,
            username=websetting.smtp_user,
            password=websetting.smtp_password,
            use_tls=use_tls,
            use_ssl=use_ssl,
            fail_silently=False
        )

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=websetting.smtp_user,
            to=recipient_list,
            connection=connection
        )
        email.send()
        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", e)