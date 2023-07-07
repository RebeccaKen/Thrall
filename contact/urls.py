from django.urls import path
from .views import contact_list

app_name = 'your_app'

urlpatterns = [
    path('contacts/', contact_list, name='contact_list'),
]