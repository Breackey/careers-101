# Generated by Django 3.2.7 on 2021-10-03 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0011_auto_20200919_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicants',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='job',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='selected',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
