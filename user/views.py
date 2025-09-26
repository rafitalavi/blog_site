from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Blog, Category
from home.models import Contact
from django.db.models import Count
from .models import Profile

from .forms import ProfileUpdateForm, UserUpdateForm, CustomPasswordChangeForm

# ==========================
# Profile Update View
# ==========================
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user/profile.html', context)

# ==========================
# Password Change View
# ==========================
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Important: Update session to keep user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('change-password')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'user/change_password.html', context)
@login_required
def admin_dashboard(request):
    categories = Category.objects.annotate(blog_count=Count('blog'))
    blog_labels = [cat.name for cat in categories]
    blog_counts = [cat.blog_count for cat in categories]
    # profile = getattr(request.user, 'profile', None)

    context = {
        'total_users': User.objects.count(),
        'total_blogs': Blog.objects.count(),
        'total_categories': Category.objects.count(),
        'total_contacts': Contact.objects.count(),
        'recent_blogs': Blog.objects.order_by('-created_at')[:5],
        'blog_labels': blog_labels,
        'blog_counts': blog_counts,
        # 'profile': profile,
    }
    return render(request, "user/dashboard.html", context)  # ✅ inside user/

def user_login(request):
    if request.user.is_authenticated:
        return redirect('user:dashboard')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('user:dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'user/login.html')
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
