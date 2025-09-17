from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("logout/", views.logout, name="logout"),
    # path(
    #     "password-change/",
    #     auth_views.PasswordChangeView.as_view(
    #         template_name="account/password_change_form.html"
    #     ),
    #     name="password_change",
    # ),
    path(
        "password-change/",
        views.CrumbsPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset_form.html",
            html_email_template_name="account/password_reset_email.html",
            email_template_name="account/password_reset_email.html",
            subject_template_name="account/password_reset_subject.txt",
            success_url=reverse_lazy("account:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html",
            success_url=reverse_lazy("account:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("edit-info/", views.UserChangeInfoView.as_view(), name="edit_info"),
    path("edit-address/", views.UserChangeAddressView.as_view(), name="edit_address"),
]
