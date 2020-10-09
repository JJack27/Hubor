from django.urls import path
from .views_user import *
from .views_test import *


urlpatterns = [
    # Accounts related
    path('emailvalidation/', EmailValidation.as_view()),
    path('usernamevalidation/', UsernameValidation.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutAPI.as_view()),

    # test
    path('test/', TestView.as_view()),

    #path('forgetpassword/', ForgetPasswordAPI.as_view()),
    #path('resetpassword/<uuid:pk>/', ResetPasswordAPI.as_view()),

]