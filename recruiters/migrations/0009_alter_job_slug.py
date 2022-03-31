# Generated by Django 4.0.1 on 2022-03-31 01:56

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0008_job_filled_alter_job_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=255, null=True, populate_from='title', unique=True),
        ),
    ]
