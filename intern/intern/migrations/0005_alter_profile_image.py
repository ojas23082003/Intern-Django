# Generated by Django 4.2.2 on 2023-06-20 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
