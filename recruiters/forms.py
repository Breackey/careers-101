from django import forms
from .models import Job
from django_summernote.widgets import SummernoteWidget


class NewJobForm(forms.ModelForm):

    description = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Job
        fields = ['title', 'company', 'location','experience','qualification','deadline','description', 'skills_req', 'job_type', 'link']
        help_texts = {
            'skills_req': 'Enter all the skills required each separated by commas.',
            'link': 'If you want candidates to apply on your company website rather than on our website, please provide the link where candidates can apply. Otherwise, please leave it blank or candidates would not be able to apply directly!',
            'deadline' : 'Enter in the format MM/DD/YYYY'
        }   
        
        

class JobUpdateForm(forms.ModelForm):

    description = forms.CharField(widget=SummernoteWidget())
    
    class Meta:
        model = Job
        fields = ['title', 'company', 'location',
                  'description', 'skills_req', 'job_type', 'link']
        help_texts = {
            'skills_req': 'Enter all the skills required each separated by commas.',
            'link': 'If you want candidates to apply on your company website rather than on our website, please provide the link where candidates can apply. Otherwise, please leave it blank or candidates would not be able to apply directly!',
        }
 