# Generated by Django 4.0.6 on 2024-10-24 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workTimeControl', '0007_alter_paidbysalary_holiday_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paidbythehour',
            name='other_hours',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidbythehour',
            name='sick_hours',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidbythehour',
            name='vacation_hours',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
