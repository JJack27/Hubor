from django.urls import path
from .views_user import *
from .views_data import *
from .views_test import *
from .views_emergency import *
from .views_config import *




urlpatterns = [
    # Accounts related
    path('emailvalidation/<str:email>/', EmailValidation.as_view()),
    path('usernamevalidation/<str:username>/', UsernameValidation.as_view()),
    path('phonevalidation/<str:phone>/', PhoneValidation.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('bracelet/<uuid:owner>/', BraceletAPI.as_view()),
    path('takecareof/<uuid:doctor>/<uuid:patient>/', TakeCareOfAPI.as_view()),
    path('patientsof/<uuid:doctor>/', PatientsOfAPI.as_view()),
    path('doctorof/<uuid:patient>/', DoctorOfAPI.as_view()),
    path('doctors/', DoctorsAPI.as_view()),
    path('shortdoctors/', ShortDoctorsAPI.as_view()),
    path('facilities/', FacilitiesAPI.as_view()),
    path('belongsto/<uuid:facility>/', BelongsToAPI.as_view()),
    path('myinfo/', MyInfoAPI.as_view()),

    # Data related
    path('data/<uuid:pk>/', DataAPI.as_view()),
    path('vitalsign/<uuid:owner>/', VitalSignAPI.as_view()),
    path('aggregatedvs/<uuid:owner>/', AggregatedVitalSignAPI.as_view()),
    

    # Emergency related
    path('emergency/<uuid:pk>/', EmergencyEventAPI.as_view()),
    path('emergencycontact/<uuid:pk>/', EmergencyContactAPI.as_view()),

    # Configuration
    path('latestconfig/', LatestConfigAPI.as_view()),

    # test
    path('test/', TestView.as_view()),
    path('allapi/', AllAPIView.as_view())

    #path('forgetpassword/', ForgetPasswordAPI.as_view()),
    #path('resetpassword/<uuid:pk>/', ResetPasswordAPI.as_view()),

]