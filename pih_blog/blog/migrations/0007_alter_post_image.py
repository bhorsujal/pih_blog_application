# Generated by Django 4.2.5 on 2023-11-06 20:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_remove_comment_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(default="default2.jpg", upload_to="post_images"),
        ),
    ]
