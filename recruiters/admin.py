from django.contrib import admin
from .models import Job, Applicants, Selected
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Job)
class JobAdmin(SummernoteModelAdmin):
    list_display = ('title', 'company', 'location','experience','qualification','deadline','description', 'skills_req', 'job_type', 'link')
    list_filter = ('recruiter', 'date_posted')
    search_fields = ('title', 'description','location','skills')
    #prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('recruiter',)
    date_hierarchy = 'date_posted'

    summernote_fields = ("description",)

admin.site.register(Selected)
admin.site.register(Applicants)
