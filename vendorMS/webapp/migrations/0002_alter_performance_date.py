# Generated by Django 5.0.4 on 2024-05-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]