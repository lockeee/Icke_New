# Generated by Django 3.0 on 2019-12-06 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_remove_warmup_save'),
    ]

    operations = [
        migrations.AddField(
            model_name='setsreps',
            name='cals_female',
            field=models.IntegerField(blank=True, help_text='Select cals', null=True),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='cals_male',
            field=models.IntegerField(blank=True, help_text='Select cals', null=True),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='distance_female',
            field=models.IntegerField(blank=True, help_text='Select meters', null=True),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='distance_male',
            field=models.IntegerField(blank=True, help_text='Select meters', null=True),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='for_max_reps',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='percentage',
            field=models.PositiveIntegerField(blank=True, help_text='Select percentage of max effort or max weight', null=True),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='percentage_plus',
            field=models.BooleanField(blank=True, default=False, help_text='Go higher if possible?'),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='reps',
            field=models.IntegerField(blank=True, default=1, help_text='Select number of sets'),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='tempo',
            field=models.CharField(blank=True, help_text='Four letters e.g 41x0', max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='weight_female',
            field=models.FloatField(blank=True, help_text='Select weight in kg', null=True),
        ),
        migrations.AddField(
            model_name='setsreps',
            name='weight_male',
            field=models.FloatField(blank=True, help_text='Select weight in kg', null=True),
        ),
    ]