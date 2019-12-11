from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    last_name = models.CharField(
        max_length=124,
    )

    first_name = models.CharField(
        max_length=124,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    date_of_birth = models.DateField()

    SEX = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    sex = models.CharField(
        max_length=1,
        choices=SEX,
        help_text='Select sex',
        default='m'
    )

    headshot = models.ImageField(
        upload_to='planner/athlete_headshots',
        default='planner/athlete_headshots/no-img.jpg',
        blank=True
    )

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('athlete-detail', args=[str(self.id)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_name = self.user.last_name
        self.first_name = self.user.first_name

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.user.last_name}, {self.user.first_name}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Track(models.Model):
    """Model representing a class type (e.g. WOD, Hyrox, Sanctional ...) """
    name = models.CharField(
        max_length=32,
        help_text='Enter a track type'
    )

    related_name = 'track'

    def __str__(self):
        """ String for representing the Model object. """
        return self.name

DEFAULT_TRACK_ID = 0

class Equipment(models.Model):
    """ Equipment needed for workout for one athlete """
    EQUIPMENT_TYPE = (
        ('kb', 'Kettlebell'),
        ('db', 'Dumbbell'),
        ('bb', 'Barbell'),
        ('c2r', 'Rower'),
        ('aab', 'AAB'),
        ('c2s', 'Ski'),
        ('box', 'Box'),
        ('c2b', 'Airbike'),
        ('ghd', 'GHD'),
        ('sb', 'Sandbag'),
        ('jr', 'Jumprope'),
        ('rig', 'Rig'),
        ('rg', 'Rings'),
    )

    equipment = models.CharField(
        max_length=3,
        choices=EQUIPMENT_TYPE,
        help_text='Select equipment'
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.equipment


class Warmup(models.Model):
    """ Model to save different warm up routines """
    """ If we give it a name and save it we can find it later """
    name = models.CharField(
        u"Name",
        max_length=64,
        blank=True,
        null=True
    )

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

    track = models.ForeignKey(
        Track,
        help_text='Enter a track',
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )

    warmup = models.TextField(
        max_length=1024,
        help_text='Warmup routine'
    )

    # Some additional stuff to do
    additional = models.TextField(
        max_length=1024,
        help_text='Add stuff to preexisting routine',
        blank = True,
    )

    equipment = models.ForeignKey(
        Equipment,
        help_text='Equipment used',
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['track', 'name']

    def _print_warmup(self):
        L = []
        if self.name:
            L.append([str(self.name)])
        else:
            L.append(["Warmup"])
        if self.additional:
            L.append([self.warmup+"\n"+self.additional])
        else:
            L.append([self.warmup])

        return L

    def __str__(self):
        """String for representing the Model object."""
        if self.name:
            return self.name
        return self.warmup

    def get_absolute_url(self):
        """Returns the url to access a detail record for this warmup."""
        return reverse(
            'warmup-detail',
            args=[str(self.id)]
        )

class MovementCategory(models.Model):

    name = models.CharField(
        u"Name",
        max_length=64,
        help_text='e.g. Squat or Pull Up',
    )

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Exercise(models.Model):

    """ Model to describe single exercise, e.g. back squat """
    name = models.CharField(
        u"Name",
        max_length=64,
        help_text='Enter an exercise'
    )

    link = models.URLField(
        blank = True,
        help_text='Enter link to explanatory video to display it if needed somewhere'
    )

    CATEGORY = (
        ('g', 'Gymnastics'),
        ('w', 'Weightlifting'),
        ('m', 'Monostructural'),
        ('s', 'Strongman'),
    )

    category = models.CharField(
        max_length=1,
        choices=CATEGORY,
        blank=True,
        null=True,
        help_text='Gymnastics, Weightlifting ...'
    )

    """ Check if push exercise """
    push = models.BooleanField(
        blank=True,
        default=False,
    )

    """ Check if pull exercise """
    pull = models.BooleanField(
        blank=True,
        default=False,
    )

    """ Check if upper body exercise """
    upper = models.BooleanField(
        blank=True,
        default=False,
    )

    """ Check if lower body exercise """
    lower = models.BooleanField(
        blank=True,
        default=False,
    )

    """ Category of exercises (e.g. squat) """
    movement_category = models.ManyToManyField(
        MovementCategory,
        verbose_name="Movement"
    )

    equipment = models.ForeignKey(
        Equipment,
        help_text='Equipment used',
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['name']

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class ExerciseSceme(models.Model):
    """ Model to describe a single exercise with reps, prescibed weights, cals .... """
    """ Backsquat 3@80kg """
    """ AAB 1min@100 watts"""

    """ Exercise to be done """
    exercise = models.ForeignKey(
        Exercise,
        help_text='Select an exercise (Snatch, HSPU ...)',
        on_delete=models.PROTECT
    )
    """ Numbers of reps per set """
    reps = models.IntegerField(
        null=True,
        blank=True,
        help_text='Select number of reps',
    )
    """ An exercise can only be for one of the following three measures, but also for none. """
    weight_male = models.FloatField(
        blank=True,
        null=True,
        help_text='Select weight in kg'
    )

    weight_female = models.FloatField(
        blank=True,
        null=True,
        help_text='Select weight in kg'
    )

    watt_male = models.IntegerField(
        null=True, blank=True,
        help_text='Select watt'
    )

    watt_female = models.IntegerField(
        null=True, blank=True,
        help_text='Select watt'
    )

    cals_male = models.IntegerField(
        null=True,
        blank=True,
        help_text='Select cals'
    )

    cals_female = models.IntegerField(
        null=True,
        blank=True,
        help_text='Select cals'
    )
    """ Distance is always saved in meters """
    distance_male = models.IntegerField(
        null=True, blank=True,
        help_text='Select meters'
    )

    distance_female = models.IntegerField(
        null=True, blank=True,
        help_text='Select meters'
    )

    time = models.DurationField(
        null=True,
        blank=True
    )

    """ Percentage of max effort or max weight """
    percentage = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Select percentage of max effort or max weight'
    )

    """ Optional tempo for exercise """
    tempo = models.CharField(
        max_length=4, blank=True,
        null=True,
        help_text='Four letters ebct e.g 41x0'
    )

    """ Plus x in each round """
    plus_x = models.IntegerField(
        blank=True,
        default=0,
        help_text='+X in each round',
    )

    """ Gives back total reps counting cals and meters as 1 reps """

    def _total_reps(self,rounds=1):
        reps = [0, 0]
        if self.reps:
            reps += [str(self.reps), str(self.reps)]
        if self.cals_male:
            reps += [str(self.cals_male), str(self.cals_female)]
        if self.distance_male:
            reps += [str(self.distance_male), str(self.distace_female)]
        if self.plus_x > 0:
            reps_rounds = [0,0]
            for i in range(rounds):
                reps_rounds += [reps[0]+(self.plus_x*i),reps[1]+(self.plus_x*i)]
        else:
            return [reps[0]*rounds,reps[1]*rounds]

    class Meta:
        ordering = ['exercise', 'reps', 'weight_male', 'cals_male', 'distance_male', 'watt_male', 'time', 'percentage',
                    'tempo']

    def _give_string(self):
        return self.__str__()

    def __str__(self):
        """String for representing the Model object."""
        string = self.exercise.__str__()
        if self.reps:
            string = str(self.reps) + " " + string
        elif self.cals_male:
            string = str(self.cals_male) + '/' + str(self.cals_female) + ' cals' + " " + string
        elif self.distance_male:
            string += str(self.distance_male) + '/' + str(self.distance_female) + ' meters'
        if self.weight_male:
            string += '@' + str(self.weight_male) + '/' + str(self.weight_female) + "kg"
        elif self.percentage:
            string += '@' + str(self.percentage) + "%"
        elif self.watt_male:
            string += '@' + str(self.watt_male) + '/' + str(self.watt_female) + " watt"
        if self.time:
            string += " for " + str(self.time)
        if self.tempo:
            string += ' (@' + self.tempo + ')'
        return string


class Block(models.Model):
    exercises = models.ManyToManyField(
        ExerciseSceme
    )

    rounds = models.PositiveIntegerField(
        blank=True,
        default=1,
    )

    """ First entry is male and second is female reps """
    def _total_reps(self,rounds=None):
        if rounds == None:
            rounds = self.rounds
        reps = [0, 0]
        for e in self.exercises.all():
            reps += e._total_reps(rounds)
        return reps

    def _total_reps_male(self,rounds=None):
        if rounds == None:
            rounds = self.rounds
        return self._total_reps(rounds)[0]

    def _total_reps_female(self,rounds=None):
        if rounds == None:
            rounds = self.rounds
        return self._total_reps(rounds)[1]

    def _print_block(self):
        string = []
        for E in self.exercises.all():
            string.append(E.__str__())
        return string

    def __str__(self):
        string = ''
        for e in self.exercises.all():
            string += e.__str__() + " "
        return string

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('block-detail', args=[str(self.id)])


class TrainingPart(models.Model):
    """ Optional name of the workout, i.e. Crossfit Open 20.1 """
    name = models.CharField(
        u"Name",
        max_length=64,
        null=True,
    )

    """ Is benchmark metcon """
    benchmark = models.BooleanField(
        blank=True,
        default=False,
        help_text='Will be stored for reuse',
    )

    SCORED_TYPE = (
        ('emom', 'EMOM'),
        ('sets', 'SetsReps'),
        ('amrap', 'AMRAP'),
        ('coup', 'Couplet'),
        ('trip', 'Triplet'),
        ('chip', 'Chipper'),
        ('free', 'FreeTraining'),
    )

    scored_type = models.CharField(
        max_length=5,
        choices=SCORED_TYPE,
        default='free',
        help_text='EMOM, AMRAP ...'
    )

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

    def _print_training_part(self):
        if self.scored_type == 'emom':
            L = self.emom._print_emom()
        elif self.scored_type == 'sets':
            L = self.setsreps._print_setsreps()
        elif self.scored_type == 'amrap':
            L = self.amrap._print_amrap()
        elif self.scored_type == 'coup':
            L = self.fortime._print_couplet()
        elif self.scored_type == 'trip':
            L = self.fortime._print_triplet()
        elif self.scored_type == 'chip':
            L = self.fortime._print_fortime()
        elif self.scored_type == 'free':
            L = self.freetraining._print_freetraining()
        if self.name:
            L = [[self.name]] + L
        return L

    def __str__(self):
        if self.scored_type == 'emom':
            return self.__str__()
        elif self.scored_type == 'sets':
            return self.setsreps.__str__()
        elif self.scored_type == 'amrap':
            return self.amrap.__str__()
        elif self.scored_type == 'coup':
            return self.fortime.__str__()
        elif self.scored_type == 'trip':
            return self.fortime.__str__()
        elif self.scored_type == 'chip':
            return self.fortime.__str__()
        elif self.scored_type == 'free':
            return self.freetraining._print_freetraining()

class TrainingPartInstance(models.Model):
    athlete = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT
    )

    """ Has this been done in RX """
    rx = models.BooleanField(
        null=True,
        default=False,
        help_text='True if RX',
    )

    training = models.ForeignKey(
        TrainingPart,
        on_delete=models.PROTECT,
    )

    """ Date the workout was done """
    date = models.DateTimeField(
        blank=True,
        default=now
    )

    def _done_rx(self):
        return self.rx


class EMOM(TrainingPart):
    """ Choose only one """
    seconds = models.IntegerField(
        null=True,
        blank=True,
        help_text='e...sos'
    )

    minutes = models.IntegerField(
        null=True, blank=True,
        help_text='e...mom'
    )

    duration = models.IntegerField(
        null=True, blank=True,
        help_text='Select duration in minutes'
    )

    exercises = models.ManyToManyField(
        Block
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scored_type = 'emom'

    def _print_emom(self):
        if self.seconds:
            L = ['E' + str(self.seconds) + "SOS " + str(self.duration)]
        else:
            L = ['E' + str(self.minutes) + "MOM " + str(self.duration)]
        for E in self.exercises.all():
            L.append(E._print_block())
        return L

    def __str__(self):
        """String for representing the Model object."""
        if self.name:
            return self.name
        else:
            string = ''
            roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
            for i in len(self.exercises):
                string += roman[i] + " " + self.exercises[i].__str__() + ' '
            if self.seconds:
                return 'E' + str(self.seconds) + "SOS for " + str(self.duration) + " " + string
            else:
                return 'E' + str(self.minutes) + "MOM for " + str(self.duration) + " " + string

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('emom-detail', args=[str(self.id)])


class EMOMInstance(TrainingPartInstance):
    """ If WorkoutPart is for reps """
    scored_reps = models.IntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['scored_reps', 'date']

    def __str__(self):
        """String for representing the Model object."""
        return str(self.scored_reps) + ' total reps in ' + str(self.training)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('emom-instace-detail', args=[str(self.id)])


class AMRAP(TrainingPart):
    """ """
    time = models.DurationField(
        null=True,
        blank=True,
        help_text='Workout time'
    )

    buyin = models.ForeignKey(
        Block,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='amrap_buyin'
    )

    exercises = models.ManyToManyField(
        Block
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scored_type = 'amrap'

    def _print_amrap(self):
        if self.buyin:
            L = [["AMRAP " + str(self.time) + " with buyin"]]
            L.append["Buyin" + '<br>' + self.buyin._print_block()]
        else:
            L = [["AMRAP " + str(self.time)]]
        for E in self.exercises.all():
            L.append(E._print_block())
        return L

    def __str__(self):
        """String for representing the Model object."""
        if self.name:
            return self.name
        else:
            string = 'AMRAP ' + str(self.time)
            if self.buyin:
                string += "Buyin: " + str(self.buyin) + " "
            string += str(self.exercises)
            return string

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('amrap-detail', args=[str(self.id)])


class AMRAPInstance(TrainingPartInstance):
    scored_rounds = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    """ If WorkoutPart is for reps """
    scored_reps = models.PositiveIntegerField()

    class Meta:
        ordering = ['scored_rounds', 'scored_reps', 'date']

    def _done_rx(self):
        return self.rx

    def __str__(self):
        """String for representing the Model object."""
        return str(self.athlete) + ' - ' + str(self.training)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('amrap-instace-detail', args=[str(self.id)])


class ForTime(TrainingPart):
    """ """
    time_cap = models.DurationField(
        null=True,
        blank=True
    )

    buyin = models.ForeignKey(
        Block, null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='fortime_buyin'
    )

    exercises = models.ManyToManyField(
        Block
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scored_type = 'chip'

    def _print_fortime(self):
        if self.buyin:
            L = [["For time " + str(self.time_cap) + " with buyin"]]
            L.append["Buyin" + '<br>' + self.buyin._print_block()]
        else:
            L = [["For time " + str(self.time_cap)]]
        for E in self.exercises.all():
            L.append(E._print_block())
        return L

    def _total_reps(self):
        reps = [0, 0]
        if self.buyin:
            reps += self.buyin._total_reps()
        for b in self.exercises.all():
            reps += b._total_reps()
        return reps

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('fortime-detail', args=[str(self.id)])


class ForTimeInstance(TrainingPartInstance):
    finnished = models.BooleanField(
        null=True,
        default=True,
        help_text='True if finished in time',
    )

    """ If WorkoutPart is for reps """
    scored_time = models.DurationField(
        blank=True,
        null=True
    )

    scored_reps = models.IntegerField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['scored_time', 'scored_reps', 'date']

    def _done_rx(self):
        return self.rx

    def __str__(self):
        """String for representing the Model object."""
        return str(self.athlete) + ' - ' + str(self.training)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('emom-instace-detail', args=[str(self.id)])


class SetsReps(TrainingPart):
    exercise = models.ForeignKey(
        Exercise,
        help_text='Select an exercise (Snatch, HSPU ...)',
        on_delete=models.PROTECT,
        verbose_name=u"Exercise"
    )

    """ Number of sets """
    sets = models.IntegerField(
        blank=True,
        help_text='Select number of sets',
        default=1
    )

    reps = models.IntegerField(
        blank=True,
        help_text='Select number of sets',
        null = True,
    )

    for_max_reps = models.BooleanField(
        blank=True,
        default=False
    )

    """ Resting time after each set is optional """
    rest = models.DurationField(
        blank=True,
        null=True,
        help_text=' - rest ... between sets'
    )

    """ An exercise can only be for one of the following three measures, but also for none. """
    weight_male = models.FloatField(
        blank=True,
        null=True,
        help_text='Select weight in kg'
    )

    weight_female = models.FloatField(
        blank=True,
        null=True,
        help_text='Select weight in kg'
    )

    cals_male = models.IntegerField(
        null=True,
        blank=True,
        help_text='Select cals'
    )

    cals_female = models.IntegerField(
        null=True,
        blank=True,
        help_text='Select cals'
    )

    """ Distance is always saved in meters """
    distance_male = models.IntegerField(
        null=True, blank=True,
        help_text='Select meters'
    )

    distance_female = models.IntegerField(
        null=True, blank=True,
        help_text='Select meters'
    )

    """ Percentage of max effort or max weight """
    percentage = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Select percentage of max effort or max weight'
    )

    percentage_plus = models.BooleanField(
        default=False,
        blank=True,
        help_text='Go higher if possible?'
    )

    """ Optional tempo for exercise """
    tempo = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        help_text='Four letters e.g 41x0'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scored_type = 'sets'

    def _print_setsreps(self):
        if self.sets > 1:
            string = str(self.sets) + "x"
        else:
            string = ""
        if self.reps:
            if self.reps > 1:
                string += str(self.reps)+ " "  + str(self.exercise) + "s"
            else:
                string += str(self.reps) + " " + str(self.exercise)
            if self.weight_male:
                # Weight
                if self.weight_female:
                    string += "@" + str(self.weight_male) + "/" + str(self.weight_female)
                else:
                    string += "@" + str(self.weight_male)
            elif self.percentage:
                # Percentage
                if self.percentage_plus:
                    string += "@" + str(self.percentage) + "% +"
                else:
                    string += "@" + str(self.percentage) + "%"
        elif self.cals_male:
            if self.cals_female:
                string += str(self.cals_male) + "/" + str(self.cals_female) + "cals "+ str(self.exercise)
            else:
                string += str(self.cals_male)+"cals "+ str(self.exercise)
        elif self.distance_male:
            if self.distance_female:
                string += str(self.distance_male) + "/" + str(self.distance_female) + "m "+ str(self.exercise)
            else:
                string += str(self.distance_male)+"m "+ str(self.exercise)
        elif self.for_max_reps:
            string += " Max " + str(self.exercise) + "s"
            if self.weight_male:
                # Weight
                if self.weight_female:
                    string += "@" + str(self.weight_male) + "/" + str(self.weight_female)
                else:
                    string += "@" + str(self.weight_male)
            elif self.percentage:
                # Percentage
                if self.percentage_plus:
                    string += "@" + str(self.percentage) + "% +"
                else:
                    string += "@" + str(self.percentage) + "%"
        if self.tempo:
            string += " @("+self.tempo+")"
        return [[string]]

    def __str__(self):
        return self._print_setsreps()[0][0]

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('setsreps-detail', args=[str(self.id)])


class SetsRepsInstance(TrainingPartInstance):
    finnished = models.BooleanField(
        null=True,
        default=True,
        help_text='True if finished in time',
    )

    def get_default_sets(self):
        return self.training.exercises.sets

    def get_default_reps(self):
        return self.training.exercises.reps

    """ Weight moved in kg """
    scored_weight = models.FloatField(
        help_text='Weight in kg'
    )

    scored_sets = models.PositiveIntegerField(
        default=get_default_sets
    )

    scored_reps = models.PositiveIntegerField(
        default=get_default_reps
    )

    class Meta:
        ordering = ['scored_weight', 'scored_reps', 'scored_sets', 'date']

    def _done_rx(self):
        return self.rx

    def __str__(self):
        """String for representing the Model object."""
        return str(self.athlete) + ' - ' + str(self.training)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('emom-instace-detail', args=[str(self.id)])


class FreeTraining(TrainingPart):
    """ Just write some text """
    description = models.TextField(
        max_length=1024,
        help_text="This wont come op in analysation and can't be scored."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scored_type = 'free'

    def _print_freetraining(self):
        return [[self.description]]

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('free-training-detail', args=[str(self.id)])


class FreeTrainingInstance(TrainingPartInstance):
    class Meta:
        ordering = ['date']

    def _done_rx(self):
        return self.rx

    def __str__(self):
        """String for representing the Model object."""
        return str(self.athlete) + ' - ' + str(self.training)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('emom-instace-detail', args=[str(self.id)])

class Workout(models.Model):
    """ Optional name of the workout, i.e. Crossfit Open 20.1 """
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    """ Optional date to do workout """
    date = models.DateField(
        default=now
    )
    """ Foreign Key used because workout can only belong to one class type, e.g. WOD, Hyrox ... """
    track = models.ForeignKey(
        Track,
        help_text='Select a category (WOD, Hyrox ...)',
        on_delete=models.PROTECT,
        default=DEFAULT_TRACK_ID
    )
    """Warmup """
    warmup = models.ManyToManyField(
        Warmup,
        help_text='Enter warmup, if necessary',
        blank=True,
    )
    """ Workout is ManyToMany because one exercise can be in multiple Workouts or Multiple times in the same """
    training = models.ManyToManyField(
        TrainingPart,
        help_text='Enter training parts'
    )
    """Warmup """
    cooldown = models.TextField(
        max_length=1024,
        help_text='Enter finnisher or cooldown, if necessary',
        null=True,
        blank=True
    )
    """ Additional information for athletes or coaches"""
    coaches_notes = models.TextField(
        max_length=1024,
        help_text='Enter coaches notes, if necessary',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['date', 'track']

    def warmup_text(self):
        return self.warmup.warmup

    def __str__(self):
        """String for representing the Model object."""
        return str(self.track) + " " + str(self.date)

    def print_workout(self):
        L = []
        if self.warmup:
            L.append(self.warmup._print_warmup())
        for TP in self.training.all():
            sL = [TP._print_training_part()]
            for s in sL:
                L.append(s)
        if self.cooldown:
            L.append([["Cooldown"], self.cooldown.splitlines()])
        if self.coaches_notes:
            L.append([["Coaches notes"], self.coaches_notes.splitlines()])
        return L

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('workout-detail-view', args=[str(self.id)])


class WorkoutInstance(models.Model):
    """ Model representing one class done by an athlete """
    athlete = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT
    )

    workout = models.ForeignKey(
        Workout,
        on_delete=models.PROTECT
    )

    """Date of workout """
    date = models.DateTimeField(
        blank=True,
        default=now
    )

    """ Notes """
    notes = models.TextField(
        max_length=1024,
        blank=True
    )

    """ Strain of workout between 1 and 10 """
    strain = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="How hard was it (1-10)?"
    )

    def track(self):
        return self.workout.track

    def __str__(self):
        """String for representing the Model object."""
        return str(self.athlete) + ' ' + str(self.workout)

    def get_absolute_url(self):
        return reverse('workout-detail', args=[str(self.id)])


