# Generated by Django 5.0.4 on 2025-01-13 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Jib', '0014_remove_order_deliver_num_customuser_deliver_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_deliver',
            name='is_accept',
            field=models.BooleanField(default=False),
        ),
    ]
