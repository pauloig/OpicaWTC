# Generated by Django 4.0.6 on 2024-08-08 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_rename_opicaemployee_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='idNumber',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
