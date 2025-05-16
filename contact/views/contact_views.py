from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from contact.models import Contact

def index(request):
    contacts_query = Contact.objects.filter(show=True).order_by('-id')
    
    paginator = Paginator(contacts_query, 30)
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)
    
    context = {
        'contacts': contacts,
        'site_title': 'Contacts'
    }
    
    return render(
        request,
        'contact/index.html',
        context
    )
    
def search(request):
    search_value = request.GET.get('q', '').strip()
    
    if not search_value:
        return redirect('contact:index')
    
    contacts_query = Contact.objects\
        .filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) | # "OR" verification
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value)
        )\
        .order_by('-id')
        
    # print(contacts.query)
    
    paginator = Paginator(contacts_query, 30)
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)
    
    context = {
        'contacts': contacts,
        'site_title': 'Search',
        'search_value': search_value,
    }
    
    return render(
        request,
        'contact/index.html',
        context
    )
    
    
def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(
        Contact, pk=contact_id, show=True
    )
    
    contact_name = f'{single_contact.first_name} {single_contact.last_name}'
    
    context = {
        'contact': single_contact,
        'site_title': contact_name,
    }
    
    return render(
        request,
        'contact/contact.html',
        context
    )
