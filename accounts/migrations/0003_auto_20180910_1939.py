# Generated by Django 2.1 on 2018-09-10 19:39

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180829_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
