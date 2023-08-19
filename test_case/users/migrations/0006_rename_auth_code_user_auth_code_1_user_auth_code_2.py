# Generated by Django 4.2.4 on 2023-08-18 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_auth_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='auth_code',
            new_name='auth_code_1',
        ),
        migrations.AddField(
            model_name='user',
            name='auth_code_2',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]