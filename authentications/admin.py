from django.contrib import admin
from .models import CustomUser
# Register your models here.

#admin.site.register(CustomUser)
#instead of the line above, we can use the decorator below to register the model in the admin panel.
#this will allow us to see the model in the admin panel and also be able to create, update, delete and view the model in the admin panel.
#we can also customize the admin panel by overriding the save_model method of the ModelAdmin class

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)