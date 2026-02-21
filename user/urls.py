from django.urls import path
from user.views import sign_up


urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    
]
