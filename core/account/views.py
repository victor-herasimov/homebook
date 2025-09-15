from django.views.generic import CreateView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from core.account.forms import UserLoginForm, UserRegistrationForm


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "account/login.html"

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("account:logout"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())


class UserRegistrationView(CreateView):
    template_name = "account/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("main:index")

    def form_valid(self, form):
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Регистрация"
        return context


@login_required
def logout(request):
    cart = request.session["cart"]
    print(request.session.session_key)
    auth.logout(request)
    if cart:
        request.session["cart"] = cart
    print(request.session.session_key)
    return redirect(reverse("main:index"))
