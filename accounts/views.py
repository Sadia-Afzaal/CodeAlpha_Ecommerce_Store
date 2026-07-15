from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from orders.models import Order

from .forms import ProfileForm, RegisterForm, StyledAuthenticationForm


def register(request):
    if request.user.is_authenticated:
        return redirect("store:home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Welcome to Aurora, {user.first_name}! Your account is ready."
            )
            return redirect("store:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


class AuroraLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True


class AuroraLogoutView(LogoutView):
    next_page = reverse_lazy("store:home")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(
        request, "accounts/profile.html", {"form": form, "orders": orders}
    )
