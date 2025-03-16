from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        CustomUser = get_user_model()
        
        try:
            # Get the user object from the email
            user = CustomUser.objects.get(email=email)           
            # Check the password with the user
            if user.check_password(password) and user.is_active:
                return user
            # if check_password(password, user.password) and user.is_active:
            #     return user
        except CustomUser.DoesNotExist:            
            return None

