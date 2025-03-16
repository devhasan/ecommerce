from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .forms import CustomUserRegistrationForm, AuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm 
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.

@login_required
def user_profile(request):
    user = request.user
    user, created = CustomUser.objects.get_or_create(email=user.email)

    if request.method == 'POST':
        #user.username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        if email != user.email:                     
            return email_change_verification(request, email, user)
        
        user.mobile = request.POST.get('mobile', user.mobile)
        user.address_line_1 = request.POST.get('address_line_1', user.address_line_1)        
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)
        user.country = request.POST.get('country', user.country)
        user.save()

        return redirect('user_profile')

    context = {
        'user_info': user,
    }
    return render(request, 'authentications/user_profile.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():                                    
        # Check if the email already exists
        # if CustomUser.objects.filter(email=email).exists():
        #     messages.error(request, "A user with that email already exists.")            
        #     return redirect('signup')

            try:
                email = form.cleaned_data.get('email')
                # Create a new user
                user = CustomUser()
                #user.is_verified = False  #Defined the default value False in the model. Assuming you have an email verification process
                user = form.save()            
                messages.success(request, f"Registration successful. Please verify your email {email}.")
                
                current_site = get_current_site(request)
                verification_link = f"http://{current_site.domain}/authentications/verify/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}"
                
                send_verification_email(user, verification_link)
                return redirect('login')
            except Exception as e:
                # Log the exception and show an error message                
                messages.error(request, f"An error occurred while creating the account.{e}")
                return redirect('signup')
        else:
            messages.error(request, "Invalid input while creating the account.")
    
    else:
        form = CustomUserRegistrationForm()        

    return render(request, 'authentications/signup.html', {'form': form})


def send_verification_email(user, verification_link):
    # Render the email template with context
    email_subject = 'Verify Your Email Address'
    email_body = render_to_string('authentications/verification_email.html', {
        'user': user,
        'verification_link': verification_link
    })

    # Create the email message
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    # Send the email
    email.content_subtype = 'html'  # Ensure the email is sent as HTML
    email.send()

@login_required
def email_change_verification(request, email, user):
    #if request.method == 'POST':
        #email = request.POST.get('email')
        #user = request.user
        user.email = email
        user.is_verified = False   # Mark user as unverified if email changes
        existing_user = CustomUser.objects.filter(email=email).exclude(id=user.id) # Check if the email already exists
        try:
            if existing_user.exists():
                messages.error(request, "A user with that email already exists.")
                return redirect('user_dashboard')
            user.save()                   
            user = request.user
            current_site = get_current_site(request)
            verification_link = f"http://{current_site.domain}/authentications/verify/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}"
            
            send_verification_email(user, verification_link)
            messages.info(request, f"Your email has been updated. Please verify your email at {user.email}")
            return redirect('login')
        
        except Exception as e:
            # Log the exception and show an error message
            print(f"Error changing email: {e}")
            messages.info(request, f"An error occurred while changing your email.{e}")
            return redirect('user_dashboard')
        
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified successfully.')
        return redirect('login')
    else:
        messages.error(request, 'The verification link is invalid or has expired.')
        return redirect('signup')


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')        
        user = authenticate(request, email=email, password=password)
        print(email, password, user)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'authentications/login.html')    
    

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = None  # Initialize the user variable
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Handle the case where the user does not exist
            print("User does not exist.")
            messages.error(request, "User does not exist.")
            return redirect('password_reset')  # Redirect to the forgot password page or another appropriate page

        if user:
            current_site = get_current_site(request)
            subject = 'Reset your password'
            verification_link = f"http://{current_site.domain}/authentications/password_reset_confirm/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}"
    
            send_password_reset_email(request, user, verification_link)
            print("Email sent")
            return redirect('login')

    return render(request, 'authentications/forgot.html')

def send_password_reset_email(request, user, verification_link):
    # Render the email template with context
    email_subject = 'Reset you password'
    email_body = render_to_string('authentications/verification_email.html', {
        'user': user,
        'verification_link': verification_link
    })

    # Create the email message
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    # Send the email
    email.content_subtype = 'html'  # Ensure the email is sent as HTML
    email.send()
    messages.success(request, 'Password reset email sent successfully.')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return redirect(f'/authentications/newpassword/{uidb64}/{token}')
    else:
        messages.error(request, 'The verification link is invalid or has expired.')
        return redirect('signup')

def newpassword(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
        print(user)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        
    if request.method == 'POST':
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('newpassword')        
        user.set_password(password)
        user.save()
        messages.success(request, 'Password updated successfully.')
        return redirect('login')
    return render(request, 'authentications/newpassword.html')

'''
@login_required #password reset from the profile page
def newpassword(request):
    if request.method == 'POST':
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('newpassword')
        user = request.user
        user.set_password(password)
        user.save()
        messages.success(request, 'Password updated successfully.')
        return redirect('login')
    return render(request, 'authentications/newpassword.html')
'''
@login_required
def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Ensure the user is authenticated
    
    user = request.user
    user_profile = user.userprofile    
    if request.method == 'POST':
        # Update user fields
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', "")
        
        print(user.email, email)
        if email != user.email:
            user.is_verified = False   # Mark user as unverified if email changes
            messages.info(request, 'Your email has been updated. Please verify your new email address.')            
            
        user.username = username
        user.email = email        
        user.save()

        # Update profile fields
        user_profile.mobile = request.POST.get('mobile', user_profile.mobile)
        user_profile.address_line_1 = request.POST.get('address_line_1', user_profile.address_line_1)
        user_profile.address_line_2 = request.POST.get('address_line_2', user_profile.address_line_2)
        user_profile.city = request.POST.get('city', user_profile.city)
        user_profile.state = request.POST.get('state', user_profile.state)
        user_profile.country = request.POST.get('country', user_profile.country)
        user_profile.save()

        return redirect('user_profile')  # Redirect to profile page after updating

    user_info = CustomUser.objects.get(id=user.id)

    # Pass the user information to the template
    context = {
        'user_info': user_info,
    }

    return render(request, 'authentications/user_profile.html', context)