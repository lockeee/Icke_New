# Generated by Django 3.0 on 2019-12-06 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_auto_20191206_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setsreps',
            name='reps',
            field=models.IntegerField(blank=True, help_text='Select number of sets', null=True),
        ),
    ]