# Generated by Django 3.2.22 on 2023-11-19 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_location_type', '0001_initial'),
        ('custom_account', '0006_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='techuserprofile',
            name='work_location_type',
            field=models.ManyToManyField(default=1, to='work_location_type.WorkLocationType'),
        ),
    ]
