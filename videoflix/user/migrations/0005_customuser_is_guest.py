# Generated by Django 5.0 on 2024-02-23 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_customuser_created_at_customuser_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_guest',
            field=models.BooleanField(default=False),
        ),
    ]