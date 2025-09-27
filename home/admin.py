from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Contact ,Banner , Websetting

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("sno", "name", "email", "phone", "date")
    search_fields = ("name", "email", "phone")
    list_filter = ("date",)
    ordering = ("-date",)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "created_at", "active")
    search_fields = ("title", "subtitle")
    list_filter = ("created_at", "active")
    ordering = ("-created_at",)   

@admin.register(Websetting) 
class WebsettingAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    # Optional: enable search by title
    search_fields = ('title',)
    
    # Optional: hide all other fields in the add/edit form (use 'fields')
    fields = ('title',)