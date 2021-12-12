from django.urls import path
from authapp.views import LoginListView, Logout, RegistrationListView, ProfileFormView

app_name = 'authapp'
urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', RegistrationListView.as_view(), name='registration'),
    path('profile/', ProfileFormView.as_view(), name='profile'),

    path('verify/<str:email>/<str:activation_key>', RegistrationListView.verify, name='verify')
]
