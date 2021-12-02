from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from users.forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

def login(request):
    return render(request, 'users/login.html')

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['careeropp101@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contact.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')


@login_required
def account(request):
    context = {
        'account_page': "active",
    }
    return render(request, 'users/account.html', context)


def privacy(request):
    return render(request, 'users/privacy.html')


def terms(request):
    return render(request, 'users/terms.html')


def pricing(request):
    context = {
        'rec_navbar': 1,
    }
    return render(request, 'users/pricing.html', context)
