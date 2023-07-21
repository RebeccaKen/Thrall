from django.urls import path
from . import views

app_name = 'contact'


urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('faq/', views.faq_page, name='faq_page'),
]