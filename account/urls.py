from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'info_users', InfoUserView)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("activate/", ActivationView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("change_password/", ChangePasswordView.as_view()),
    path("forgot_password/", ForgotPasswordView.as_view()),
    path("forgot_password_complete/", ForgetCompletePasswordView.as_view()),
    path('', include(router.urls)),
]