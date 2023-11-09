# Generated by Django 3.2.22 on 2023-11-08 15:54

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_account', '0003_alter_recruiteruserprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
