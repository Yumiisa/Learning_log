from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method != "POST":
        # display blank registration form
        form = UserCreationForm()
    else:
        # process a completed form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # log the user in and redirect to home page
            authenticated_user = authenticate(
                username=new_user.username, password=request.POST["password1"]
            )
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse("home"))
    context = {"form": form}
    return render(request, "users/register.html", context)
