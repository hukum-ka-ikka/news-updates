# Generated by Django 4.2.16 on 2024-11-30 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("automation_backend", "0002_feedmodel_image_alter_feedmodel_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedmodel", name="image", field=models.URLField(),
        ),
    ]
