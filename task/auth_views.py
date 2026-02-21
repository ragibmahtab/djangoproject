from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        role = request.POST.get("role", "").strip()

        if not username or not email or not password or not role:
            return render(request, "signup.html", {
                "error": "All fields are required."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already taken. Try another."
            })

        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {
                "error": "Email already registered."
            })

        # Create user — NOT active yet
        user = User(
            username=username,
            email=email,
            first_name="",
            last_name="",
            is_active=False
        )
        user.set_password(password)
        user.save()

        # Assign group
        try:
            group = Group.objects.get(name=role)
            user.groups.add(group)
        except Group.DoesNotExist:
            return render(request, "signup.html", {
                "error": "Selected role does not exist. Contact admin."
            })

        # Generate activation token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build activation link
        activation_link = request.build_absolute_uri(
            f"/activate/{uid}/{token}/"
        )

        # Send activation email to the email user entered in signup form
        try:
            send_mail(
                subject="Activate Your Elluminate Account",
                message=f"""
Hi {username},

Thank you for signing up on Elluminate!

Please click the link below to activate your account:

{activation_link}

If you did not sign up, ignore this email.

Thanks,
Elluminate Team
                """,
                from_email=None,  # uses DEFAULT_FROM_EMAIL from settings.py
                recipient_list=[email],  # sends to the email entered in signup form
                fail_silently=False,
            )
        except Exception as e:
            print("Email error:", e)
            return render(request, "signup.html", {
                "error": "Account created but email could not be sent. Contact admin."
            })

        return render(request, "signup.html", {
            "message": f"Account created! Activation link sent to {email}. Please check your inbox."
        })

    return render(request, "signup.html")


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "login.html", {
            "message": "Account activated successfully! You can now login."
        })
    else:
        return render(request, "login.html", {
            "error": "Invalid or expired activation link."
        })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "login.html", {
                "error": "No account found with this username."
            })

        if not user_obj.is_active:
            return render(request, "login.html", {
                "error": "Account not activated. Please check your email inbox."
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser or user.groups.filter(name="Admin").exists():
                return redirect("admin_dashboard")
            elif user.groups.filter(name="Organizer").exists():
                return redirect("organizer_dashboard")
            elif user.groups.filter(name="Participant").exists():
                return redirect("participant_dashboard")
            else:
                return render(request, "login.html", {
                    "error": "No role assigned. Contact admin."
                })
        else:
            return render(request, "login.html", {
                "error": "Wrong password. Please try again."
            })

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")