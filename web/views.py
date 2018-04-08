from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def home(request):
    template = loader.get_template('home.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template('about.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def projects(request):
    template = loader.get_template('projects.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


# def contact(request):
#     template = loader.get_template('contact.html')
#     context = {
#
#     }
#     return HttpResponse(template.render(context, request))
#
#
# def contactSend(request):
#     return render(request, 'contact.html', {'form': form})

# pip install django-widget-tweaks

from .models import ContactForm
from django.core.mail import BadHeaderError, EmailMessage
from django.shortcuts import redirect

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            content = form.cleaned_data['content']
            try:
                email = EmailMessage(contact_name,
                                    content,
                                    contact_email,
                                    ['youremail@gmail.com'], #change to your email
                                     reply_to=[contact_email],
                                   )
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('./thanks/')
    return render(request, 'contact.html', {'form': form})


def thanks(request):
    return render(request, 'thanks.html', {})