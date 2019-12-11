# Generated by Django 2.2.8 on 2019-12-10 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planner', '0017_auto_20191210_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('sex', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default='m', help_text='Select sex', max_length=1)),
                ('headshot', models.ImageField(blank=True, default='planner/athlete_headshots/no-img.jpg', upload_to='planner/athlete_headshots')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.AlterField(
            model_name='trainingpartinstance',
            name='athlete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planner.Profile'),
        ),
        migrations.AlterField(
            model_name='workoutinstance',
            name='athlete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planner.Profile'),
        ),
        migrations.DeleteModel(
            name='Athlete',
        ),
    ]
