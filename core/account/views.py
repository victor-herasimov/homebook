from django.utils.functional import cached_property
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from view_breadcrumbs import BaseBreadcrumbMixin
from core.account.forms import UserChangeInfoForm, UserLoginForm, UserRegistrationForm


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
    auth.logout(request)
    if cart:
        request.session["cart"] = cart
    return redirect(reverse("main:index"))


class ProfileView(BaseBreadcrumbMixin, TemplateView):
    template_name = "account/profile.html"

    @cached_property
    def crumbs(self):
        return [("Особистий кабінет", reverse("account:profile"))]


class CrumbsPasswordChangeView(BaseBreadcrumbMixin, PasswordChangeView):
    template_name = "account/password_change_form.html"

    @cached_property
    def crumbs(self):
        return [
            ("Особистий кабінет", reverse("account:profile")),
            ("Зінити пароль", reverse("account:password_change")),
        ]

    def form_valid(self, form):
        messages.info(self.request, "Пароль успішно змінено!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Виникла помилка!")
        return super().form_invalid(form)


class UserChangeInfoView(BaseBreadcrumbMixin, LoginRequiredMixin, UpdateView):
    template_name = "account/edit_info.html"
    form_class = UserChangeInfoForm
    success_url = reverse_lazy("account:edit_info")

    @cached_property
    def crumbs(self):
        return [
            ("Особистий кабінет", reverse("account:profile")),
            ("Редагувати інформацію", reverse("account:edit_info")),
        ]

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.info(self.request, "Дані успішно змінено!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Виникла помилка!")
        return super().form_invalid(form)
