# Generated by Django 5.0.4 on 2025-01-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Jib', '0012_rename_is_it_banned_customuser_is_ban'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_deliver',
            name='num',
            field=models.IntegerField(default=0),
        ),
    ]
