# Generated by Django 4.2.5 on 2023-11-06 19:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_alter_post_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="user",
        ),
    ]
