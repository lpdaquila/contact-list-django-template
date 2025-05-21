from django.urls import path
from contact.views import \
    index, contact, search, \
    create, update, delete, \
    register, login_view, logout_view, \
    user_update

app_name = 'contact'

urlpatterns = [
    path('search/', search, name='search'),
    path('', index, name='index'),
    
    # contact (CRUD)
    path('contact/<int:contact_id>/', contact, name='contact'),
    path('contact/create/', create, name='create'),
    path('contact/<int:contact_id>/update/', update, name='update'),
    path('contact/<int:contact_id>/delete/', delete, name='delete'),
    
    # user 
    path('user/create/', register, name='register'), 
    path('user/login/', login_view, name='login'), 
    path('user/logout/', logout_view, name='logout'), 
    path('user/update/', user_update, name='user_update'), 
]