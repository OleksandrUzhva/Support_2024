# Generated by Django 4.2.11 on 2024-05-04 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_is_active_activationkey"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activationkey",
            name="key",
            field=models.UUIDField(null=True),
        ),
    ]
