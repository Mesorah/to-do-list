# Generated by Django 5.0.7 on 2024-08-04 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tdl', '0005_remove_itemlist_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemlist',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
