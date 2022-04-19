from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Newsletter, NewsletterUser
from .forms import NewsletterUserSubscribeForm, NewsletterCreationForm

from django.core.exceptions import PermissionDenied
from debug.decorators import log_exceptions
 


@log_exceptions('newsletter_subscribe')
def newsletter_subscribe(request):
    form = NewsletterUserSubscribeForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 
                                "You are already Subscribed to our Newsletter!", 
                                "alert alert-warning alert-dismissible")
        else:
            instance.save()
            messages.success(request,
                                'Thank you for subscribing to our Newsletter!',
                                "alert alert-success alert-dismissible")

            subject = "Thank you for subscribing to our Newsletter!"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(str(settings.BASE_DIR) + "/newsletter/templates/newsletters/subscribe_email.txt") as f:
                subscribe_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=subscribe_message, from_email = from_email, to=to_email)
            html_template = get_template("newsletters/subscribe_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()

    context = {
            'form':form
        }

    template = "newsletters/subscribe.html"
    return render(request,template,context)

@log_exceptions('newsletter_unsubscribe')
def newsletter_unsubscribe(request):
    form = NewsletterUserSubscribeForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request,
                                'You have successfully unscubscribed to our Newsletter!',
                                "alert alert-success alert-dismissible")

            subject = "You have successfully unsubscribed to our Newsletter!"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(str(settings.BASE_DIR) + "/newsletter/templates/newsletters/unsubscribe_email.txt") as f:
                unsubscribe_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=unsubscribe_message, from_email = from_email, to=to_email)
            html_template = get_template("newsletters/unsubscribe_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()
        else:
            messages.warning(request, 
                                "You are not Subscribed to our Newsletter!", 
                                "alert alert-warning alert-dismissible")

    context = {
        'form':form
        }

    template = "newsletters/unsubscribe.html"
    return render(request,template,context)

@log_exceptions('control_newsletter')
def control_newsletter(request):
   
    form = NewsletterCreationForm(request.POST or None)

    if form.is_valid():
        instance = form.save()
        newsletter = Newsletter.objects.get(id=instance.id)

        if newsletter.status == "Published":
            subject = newsletter.subject
            body = newsletter.body
            from_email = settings.EMAIL_HOST_USER
            for email in newsletter.email.all():
                send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)

    context = {
            "form":form,
                }

    template = 'control_panel/control_newsletter.html'
    return render(request, template, context)

@log_exceptions('control_newsletter_list')
def control_newsletter_list(request):
    newsletters = Newsletter.objects.all()
    paginator = Paginator(newsletters,10)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number-1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index>= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'items' : items,
        'page_range' : page_range
            }

    template = 'control_panel/control_newsletter_list.html'
    return render(request, template, context)

@log_exceptions('control_newsletter_detail')
def control_newsletter_detail(request,pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    context ={
        'newsletter': newsletter
    }

    template = 'control_panel/control_newsletter_detail.html'
    return render(request, template, context)

@log_exceptions('control_newsletter_edit')
def control_newsletter_edit(request,pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)

        if form.is_valid():
            newsletter = form.save()
            if newsletter.status == "Published":
                subject = newsletter.subject
                body = newsletter.body
                from_email = settings.EMAIL_HOST_USER
                for email in newsletter.email.all():
                    send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)
    
            return redirect('control_panel:control_newsletter_detail', pk=newsletter.pk)

    else:
        form = NewsletterCreationForm(instance=newsletter)

    context ={
        'form': form
    }

    template = 'control_panel/control_newsletter.html'
    return render(request, template, context)

@log_exceptions('control_newsletter_delete')
def control_newsletter_delete(request,pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)

        if form.is_valid():
            newsletter.delete()
            return redirect('control_panel:control_newsletter_list')

    else:
        form = NewsletterCreationForm(instance=newsletter)

    context ={
        'form': form
    }

    template = 'control_panel/control_newsletter_delete.html'
    return render(request, template, context)