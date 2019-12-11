# forms.py
from django.forms import ModelForm
from .models import *


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('sex', 'date_of_birth', 'headshot')


class SetsRepsForm(ModelForm):
    class Meta:
        model = SetsReps
        fields = ('exercise','tempo','benchmark' ,'sets','reps','for_max_reps',
                         'weight_male','weight_female','cals_male','cals_female','distance_male',
                         'distance_female','percentage','percentage_plus')

class WorkoutInstanceForm(ModelForm):
    class Meta:
        model = WorkoutInstance
        fields = ['athlete', 'workout', 'date', 'notes', 'strain']

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['track', 'date', 'warmup', 'training', 'cooldown','coaches_notes']

class SingleChoiceForm(ModelForm):
    class Meta:
        model = TrainingPart
        fields = ['scored_type']
