# Generated by Django 4.2.4 on 2023-08-18 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='invite_code',
            field=models.CharField(blank=True, default=1, max_length=6, unique=True),
            preserve_default=False,
        ),
    ]
