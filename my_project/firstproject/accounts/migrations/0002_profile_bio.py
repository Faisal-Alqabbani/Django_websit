# Generated by Django 2.2.3 on 2019-08-09 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(max_length=400, null=True),
        ),
    ]
