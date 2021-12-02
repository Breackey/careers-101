from django.urls import path
from newsletter import views

app_name = "control_panel"

urlpatterns = [
    path('newsletter/', views.control_newsletter, name='control_newsletter'),
    path('newsletter-list/', views.control_newsletter_list, name='control_newsletter_list'),
    path('newsletter-detail/<int:pk>', views.control_newsletter_detail, name='control_newsletter_detail'),
    path('newsletter-edit/<int:pk>', views.control_newsletter_edit, name='control_newsletter_edit'),
    path('newsletter-delete/<int:pk>', views.control_newsletter_delete, name='control_newsletter_delete'),

   
]
