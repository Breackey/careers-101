from django.db import models
from users.models import User
from django.utils import timezone
from autoslug import AutoSlugField
from django_countries.fields import CountryField
from django.utils import timezone


CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Contract', 'Contract'),
    ('Permanent','Permanent'),
    ('Internship', 'Internship'),
    ('Attachment', 'Attachment'),
    
)

QUALIFICATIONS = (
    ('High Scool Certificate', 'High Scool Certificate',),
    ('Diploma', 'Diploma'),
    ('Degree', 'Degree'),
    ('Masters', 'Masters'),
)

class Job(models.Model):
    recruiter = models.ForeignKey(
        User, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    description = models.TextField()
    experience = models.IntegerField(null=True, blank=True)
    qualification = models.CharField(max_length=30, choices=QUALIFICATIONS, default='None', null=True, blank=True)
    skills_req = models.CharField(max_length=200)
    job_type = models.CharField(max_length=30, choices=CHOICES, default='Full Time', null=True)
    link = models.URLField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True, max_length=255)
    date_posted = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(null=True, blank=True)
    filled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-date_posted',)
    
    def __str__(self):
        return self.title


class Applicants(models.Model):
    job = models.ForeignKey(
        Job, related_name='applicants', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='applied', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.applicant


class Selected(models.Model):
    job = models.ForeignKey(
        Job, related_name='select_job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='select_applicant', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.applicant
