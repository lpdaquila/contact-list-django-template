from django.urls import path
from contact.views import index, contact, search

app_name = 'contact'

urlpatterns = [
    path('<int:contact_id>/', contact, name='contact'),
    path('search/', search, name='search'),
    path('', index, name='index'),
]