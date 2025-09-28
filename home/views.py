from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, BannerForm
from .models import Banner, Websetting ,Contact
from blog.models import Blog
from django.core.mail import EmailMessage, get_connection

def send_dynamic_email(subject, message, recipient_list):
    websetting = Websetting.objects.first()
    if not websetting or not websetting.smtp_host:
        print("SMTP settings not configured")
        return

    try:
        connection = get_connection(
            host=websetting.smtp_host,
            port=websetting.smtp_port,
            username=websetting.smtp_user,
            password=websetting.smtp_password,
            use_tls=websetting.smtp_use_tls,
            use_ssl=websetting.smtp_use_ssl,
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


def home(request):
    banner = Banner.objects.all()
    blogs = Blog.objects.filter(published=True)[:4]
    websetting = Websetting.objects.first()

    form = ContactForm(request.POST or None)
    if request.method == "POST":
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
            messages.success(request, "Your message has been sent successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors in the form.")

    context = {
        'banner': banner,
        'blogs': blogs,
        'form': form,
        'websetting': websetting
    }
    return render(request, 'home/home.html', context)

def about(request): return render(request, 'home/about.html')
def contact(request):
    websetting = Websetting.objects.first()
    if not websetting or not websetting.smtp_host:
        print("SMTP settings not configured")
        return
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            contact_instance = form.save()
            send_dynamic_email(
                subject="New Contact Message",
                message=f"From: {contact_instance.name}\nEmail: {contact_instance.email}\nMessage: {contact_instance.message}",
                recipient_list=[websetting.email]
            )
            send_dynamic_email(
                subject="We Received Your Message",
                message=f"Hello {contact_instance.name},\n\nThank you for contacting us! We have received your message and will get back to you shortly.\n\nBest regards,\n{websetting.title}",
                recipient_list=[contact_instance.email]
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors in the form.")

    context = {
        'form': form,
        'websetting': websetting
    }
    return render(request, 'home/contact.html', context)


@login_required
def banner_create(request):
    form = BannerForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Banner created successfully.")
        return redirect('user:all_banner')
    return render(request, 'home/banner_form.html', {'form': form, 'title': 'Create Banner'})


@login_required
def banner_edit(request, id):
    banner = get_object_or_404(Banner, id=id)
    form = BannerForm(request.POST or None, request.FILES or None, instance=banner)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Banner updated successfully.")
        return redirect('user:all_banner')
    return render(request, 'home/banner_form.html', {'form': form, 'title': 'Edit Banner'})


@login_required
def banner_delete(request, id):
    banner = get_object_or_404(Banner, id=id)
    if request.method == 'POST':
        banner.delete()
        messages.success(request, "Banner deleted successfully.")
        return redirect('user:all_banner')

@login_required
def contact_delete(request, id):
    contact = get_object_or_404(Contact, sno=id)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Contact deleted successfully.")
        return redirect('user:all_contact_form')
