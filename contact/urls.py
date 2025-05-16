from django.urls import path
from contact.views import index, contact, search, create

app_name = 'contact'

urlpatterns = [
    path('search/', search, name='search'),
    path('', index, name='index'),
    
    # contact (CRUD)
    path('contact/<int:contact_id>/', contact, name='contact'),
    path('contact/create/', create, name='create'),
    path('contact/<int:contact_id>/update/', contact, name='contact'),
    path('contact/<int:contact_id>/delete/', contact, name='contact'),
]