from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages, auth
from django.views.generic import CreateView, FormView, RedirectView
from users.forms import *
from users.models import User
from debug.decorators import log_exceptions
from django.utils.decorators import method_decorator


@method_decorator(log_exceptions, name='post')
class RegisterEmployeeView(CreateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = 'account/candidate/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super(RegisterEmployeeView,self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('account_login')
        else:
            return render(request, 'account/candidate/register.html', 
                        {'form': form,
                        'candidate_regiser': "active",})


@method_decorator(log_exceptions, name='post')
class RegisterEmployerView(CreateView):
    model = User
    form_class = EmployerRegistrationForm
    template_name = 'account/recruiter/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    #@log_exceptions('post')
    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('account_login')
        else:
            return render(request, 'account/recruiter/register.html', 
                            {'form': form,
                            'recruiter_register': "active",})

@log_exceptions('login')
def login(request):
    return render(request, 'account/login.html')

""" def contactView(request):
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
    return render(request, "users/contact.html", {'form': form}) """

@log_exceptions('successView')
def successView(request):
    return HttpResponse('Success! Thank you for your message.')

@log_exceptions('account')
@login_required
def account(request):
    context = {
        'account_page': "active",
    }
    return render(request, 'users/account.html', context)

@log_exceptions('privacy')
def privacy(request):
    return render(request, 'users/privacy.html')

@log_exceptions('terms')
def terms(request):
    return render(request, 'users/terms.html')

@log_exceptions('pricing')
def pricing(request):
    return render(request, 'users/pricing.html')