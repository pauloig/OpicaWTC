# Generated by Django 4.0.6 on 2024-08-20 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0014_alter_employee_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='paidByTheHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('clockIn', models.TimeField(blank=True, null=True)),
                ('clockOut', models.TimeField(blank=True, null=True)),
                ('breakIn', models.TimeField(blank=True, null=True)),
                ('breakOut', models.TimeField(blank=True, null=True)),
                ('lunchIn', models.TimeField(blank=True, null=True)),
                ('lunchOut', models.TimeField(blank=True, null=True)),
                ('total_hours', models.FloatField(blank=True, null=True)),
                ('regular_hours', models.FloatField(blank=True, null=True)),
                ('double_time', models.FloatField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('createdBy', models.CharField(blank=True, max_length=60, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('updatedBy', models.CharField(blank=True, max_length=60, null=True)),
                ('EmployeeID', models.ForeignKey(db_column='EmployeeID', on_delete=django.db.models.deletion.CASCADE, to='catalog.employee')),
            ],
            options={
                'unique_together': {('date', 'EmployeeID')},
            },
        ),
    ]
