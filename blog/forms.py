from django import forms
from .models import Blog , Category, SubCategory

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title',
            'content',
            'author',
            'published',
            'image',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'meta_image',
            'category',
            'subcategory',
            'slug',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter blog title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your blog content here...',
                'rows': 10
            }),
         
            'author': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Author name'
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Meta title (max 160 characters)'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Meta description (max 160 characters)',
                'rows': 3
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Meta keywords, comma-separated'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'URL Slug (auto-generated if left blank)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subcategory': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_meta_title(self):
        meta_title = self.cleaned_data.get('meta_title')
        if meta_title and len(meta_title) > 160:
            raise forms.ValidationError("Meta title must be 160 characters or less.")
        return meta_title

    def clean_meta_description(self):
        meta_description = self.cleaned_data.get('meta_description')
        if meta_description and len(meta_description) > 160:
            raise forms.ValidationError("Meta description must be 160 characters or less.")
        return meta_description

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description' ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Category Name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Category Slug'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Category Description',
                'rows': 3
            }),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Category with this name already exists.")
        return name
    

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'description']  # exclude slug, since it's auto-generated
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SubCategory Name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'SubCategory Description',
                'rows': 3,
            }),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Subcategory with this name already exists.")
        return name