# Generated by Django 2.2.4 on 2019-08-20 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
