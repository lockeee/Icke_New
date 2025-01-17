# Generated by Django 3.0 on 2019-12-06 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0007_auto_20191206_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='training',
            field=models.ManyToManyField(help_text='Enter training parts', to='planner.TrainingPart'),
        ),
        migrations.DeleteModel(
            name='Training',
        ),
    ]
