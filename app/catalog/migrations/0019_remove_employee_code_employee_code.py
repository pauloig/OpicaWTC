# Generated by Django 4.0.6 on 2024-09-10 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='code',
        ),
        migrations.AddField(
            model_name='employee',
            name='Code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.code'),
        ),
    ]
