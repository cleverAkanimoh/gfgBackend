from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gfg import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token

# Create your views here
def home(request):
    return render(request, 'index.html')

def back(request):
    return redirect('home')

def remember(request):
    return User

def signup(request):
    if request.method=='POST':
        username    = request.POST.get('username')
        fname       = request.POST.get('fname')
        lname       = request.POST.get('lname')
        email       = request.POST.get('email')
        pass1       = request.POST.get('pass1')
        pass2       = request.POST.get('pass2')

        if User.objects.filter(username = username):
            messages.error(request, 'Username already exist')
            return redirect('signup')
        
        if User.objects.filter(email = email):
            messages.error(request, 'Email address is already registered')
            return redirect('signup')

        if len(username)>10:
            messages.error(request, 'Username must be less than 10 Characters')

        if pass1 != pass2:
            messages.error(request, 'password does not match')

        #if not username.isa1num():
            #messages.error(request, 'Username must be Alphanumeric')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.pass2       = pass2
        myuser.first_name  = fname
        myuser.last_name   = lname
        myuser.is_active   = False
        myuser.save()

        messages.success(request, 'your account has been successfully created, Please check your mail to activate your account')

        # Welcome Email

        subject     = 'Welcome to Clever Akanimoh\'s Trade ABC'
        message     = 'Hello ' + myuser.first_name + '\n \n' + 'Welcome to Clever Akanimoh\'s Trade ABC Testing Site. | |\n \nThank you for visiting our website !\n \nWe have sent your confirmation email. Please use it to confirm your Email Address inorder to activate your account.\n \nThanking you\n \n \n Mark Akpan\nFor Trade ABC.'
        from_email = settings.EMAIL_HOST_USER
        to_list     = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently = True)

        # Email Address Confirmation

        current_site  = get_current_site(request)
        email_subject = 'Confirm your Email Address @ Trade ABC | '
        message2      = render_to_string('email_confirmation.html',{
            'fname': myuser.first_name,
            'lname': myuser.last_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username    = request.POST['username']
        pass1       = request.POST['pass1']

        user        = authenticate(username = username, password = pass1)

        if user is not None:
            login(request, user)
            fname=user.first_name
            lname=user.last_name
            return render(request, 'page2.html', {
                'fname':fname,
                'lname':lname
            })
        else:
            messages.error(request, 'Bad credentials!, Try again')
            return redirect("signin")

    return render(request, 'signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'logout successful')
    return redirect('home')

def delete(request):
    myuser = User.objects.get(username=myuser.username).delete()
    messages.info(request, 'your account has been deleted, Register Again')
    return redirect('signin')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        fname=myuser.first_name
        lname=myuser.last_name
        messages.success(request, 'Activation successful')
        return redirect('page2', {
                'fname':fname,
                'lname':lname,
            })
    else:
        return render(request, 'activation_failed.html')
        