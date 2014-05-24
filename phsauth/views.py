from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_page(request):
    context = { "path": request.GET.get("next","/") }
    username = request.POST.get("username")
    password = request.POST.get("password")
    context["username"] = username if username else ""
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
        else:
            context["message"] = "Disabled account!"
    elif username is not None or password is not None:
        context["message"] = "Invalid username/password!"

    if request.user.is_authenticated():
        return redirect(request.GET.get("next","/"))
    else:
        return render_to_response("login.html", context)


def logout_page(request):
    logout(request)
    return redirect("/")

@login_required
def change_password(request):
    context = { "message": "" }
    old_password = request.POST.get("old-password")
    password = request.POST.get("new-password","")

    if old_password:
        if request.user.check_password(old_password):
            if password == request.POST.get("new-password-1"):
                if len(password.strip()) < 4:
                    context["message"] = "New password is too short!"
                else:
                    request.user.set_password(password)
                    request.user.save()
                    context["message"] = "success"
            else:
                context["message"] = "Passwords do not match!"
        else:
            context["message"] = "Incorrect old password!"
    
    if context["message"] == "success":
        return redirect("/")
    else:
        return render_to_response("change-password.html", context)
