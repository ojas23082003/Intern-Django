# Generated by Django 4.2.2 on 2023-06-28 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0015_appointment_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='speciality',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
