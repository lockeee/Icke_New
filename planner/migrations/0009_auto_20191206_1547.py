# Generated by Django 3.0 on 2019-12-06 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0008_auto_20191206_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='movement_category',
            field=models.ManyToManyField(to='planner.MovementCategory', verbose_name='Movement'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='movementcategory',
            name='name',
            field=models.CharField(help_text='e.g. Squat or Pull Up', max_length=64, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='setsreps',
            name='exercise',
            field=models.ForeignKey(help_text='Select an exercise (Snatch, HSPU ...)', on_delete=django.db.models.deletion.PROTECT, to='planner.Exercise', verbose_name='Exercise'),
        ),
        migrations.AlterField(
            model_name='trainingpart',
            name='name',
            field=models.CharField(max_length=64, null=True, verbose_name='Name'),
        ),
    ]
