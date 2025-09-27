from django import forms
from .models import Contact , Websetting

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("⚠️ Email is required. Please provide an email address.")
        return email


class WebsettingForm(forms.ModelForm):
    class Meta:
        model = Websetting
        fields = [
            'title', 'email', 'phone', 'address', 'facebook', 'linkedin', 'instagram',
            'twitter', 'google_map', 'short_descriptions', 'meta_title', 'meta_description',
            'meta_image', 'logo', 'fav_image', 'google_analytics_id'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
           'google_map': forms.Textarea(attrs={
    'class': 'form-control',
    'rows': 4,
    'placeholder': 'Paste Google Maps iframe code here'
}),
            'short_descriptions': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'meta_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'fav_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'google_analytics_id': forms.TextInput(attrs={'class': 'form-control'}),
        }