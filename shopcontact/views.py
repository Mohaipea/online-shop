from typing import Optional, Any
from shopsetting.models import ShopSetting
from django.shortcuts import render
from .forms import ContactForm
from .models import Contact


def contactPage(request):
    setting = ShopSetting.objects.first()
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        # todo : show user a success message
        form = ContactForm()

    context = {'contact_form': form, 'setting': setting}
    return render(request, 'shopcontact/contactus.html', context)
