# Generated by Django 4.2.17 on 2025-03-31 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
