import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from datetime import datetime,timedelta
from .forms import *
from jet.admin import CompactInline

admin.site.register(Track)
admin.site.register(Equipment)
admin.site.register(Block)
admin.site.register(EMOM)
admin.site.register(AMRAP)
admin.site.register(ForTime)
admin.site.register(FreeTraining)
admin.site.register(EMOMInstance)
admin.site.register(AMRAPInstance)
admin.site.register(SetsRepsInstance)
admin.site.register(ForTimeInstance)
admin.site.register(FreeTrainingInstance)

class WorkoutInstanceInline(CompactInline):
    model = WorkoutInstance
    extra = 0


# Define the admin class
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth')
    readonly_fields = ('user','first_name','last_name')
    fieldsets = (
        (None, {
            'fields': (('last_name','first_name'),'date_of_birth','user','headshot'),
        }),
    )
    inlines = [WorkoutInstanceInline]

# Register the admin class with the associated model
admin.site.register(Profile, ProfileAdmin)

@admin.register(MovementCategory)
class MovementCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    filter_horizontal = [
        'movement_category',
    ]
    list_display = ('name', 'category','equipment', 'upper','lower' , 'push','pull')
    list_editable = ( 'upper','lower' , 'push','pull')
    list_filter = ('category','movement_category')
    radio_fields = {"category": admin.HORIZONTAL}
    autocomplete_fields = ['movement_category']
    fieldsets = (
        (None, {
            'fields': (('name','link'),),
        }),
        ("Categorizing", {
            'fields': ('category',('upper','lower' , 'push','pull') ,( 'movement_category', 'equipment'))
        }),
    )

class TrainingPartInLine(CompactInline):
    model = Workout.training.through
    verbose_name = "TraingPart"
    verbose_name_plural = "TraingParts"
    extra = 0

class WarmupInLine(CompactInline):
    model = Workout.warmup.through
    extra = 0
    verbose_name = "Warmup"
    verbose_name_plural = "Warmup"

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    form = WorkoutForm
    list_display = ('track', 'date')
    list_filter = ('track', 'date')
    fieldsets = (
        ("Info", {
            'fields': ('track', 'date'),
        }),
        # ("Warmup", {
        #     'fields': ['warmup'],
        # }),
        # ('Training', {
        #     'fields': ['training'],
        # }),
        ('Extras', {
            'fields': ('cooldown', 'coaches_notes'),
            'classes': ['collapse'],
        })
    )
    inlines = [WarmupInLine,TrainingPartInLine]

    # change_form_template = 'admin/planner/workout/change_form.html'


    def add_view(self, request, extra_context=None):

        # Call the superclass changelist_view to render the page
        return super().add_view(request)

    def changelist_view(self, request, extra_context=None):
        # Return all Workouts in the surrounding 8 weeks
        d = datetime.now()
        t = timedelta(weeks=4)
        last = d - t
        next = d + t
        workouts = Workout.objects.filter(date__range=[last, next])
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context={'workouts': workouts})

@admin.register(WorkoutInstance)
class WorkoutInstanceAdmin(admin.ModelAdmin):
    list_display = ('track', 'date','athlete')
    list_filter = [
        'date'
    ]

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            WorkoutInstance.objects.annotate(day=TruncDay("date"))
                .values("day")
                .annotate(y=Count("id"))
                .order_by("-day")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(TrainingPart)
class TrainingPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'scored_type', 'benchmark')
    fields = [('name', 'scored_type', 'benchmark')]

@admin.register(SetsReps)
class SetsRepsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['exercise']
    list_display = ('exercise','sets', 'reps','weight_male' ,'cals_male', 'distance_male', 'percentage' , 'tempo')
    fields = [ ('exercise','tempo','benchmark'),('sets','reps','for_max_reps'),('weight_male','weight_female'),('cals_male','cals_female'),
               ('distance_male','distance_female'),('percentage','percentage_plus')]
    change_list_template = "admin/change_list.html"

@admin.register(Warmup)
class WarmupAdmin(admin.ModelAdmin):
    list_display = ('name', 'track', 'warmup')
    fields = ['name', ('track', 'equipment'),'warmup' ,'additional']
    search_fields = ['name']
