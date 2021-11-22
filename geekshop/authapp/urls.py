from django.urls import path
from authapp.views import login, logout, registration

app_name = 'authapp'
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
]
