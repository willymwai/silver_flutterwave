# Generated by Django 4.2 on 2023-04-27 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silver_flutterwave', '0008_card_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]