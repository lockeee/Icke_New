from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from django.utils.timezone import now

def index(request):
    """View function for home page of site."""

    # Show the WOD of the day and more
    # today = datetime.today()
    # wod_today = Workout.objects.filter(date__exact=today)

    date = now().date()
    today = Workout.objects.filter(date=date, track__name="WOD").first()
    if today:
        wod_today = today.print_workout()
        context = {
            'wod_today': wod_today,
        }
    else:
        context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# @login_required(login_url='/accounts/login/')
class WhiteboardView(generic.ListView):
    model = TrainingPartInstance
    template_name = 'whiteboard.html'
    context_object_name = 'whiteboard_list'

    def get_queryset(self):
        return TrainingPartInstance.objects.filter(date__gt=now().date())


# @login_required(login_url='/accounts/login/')
class TrainingPartInstanceDetailView(generic.ListView):
    model = TrainingPartInstance
    template_name = 'training-part-instance_detail.html'
    context_object_name = 'one_instance'

def is_coach(user):
    return user.groups.filter(name__in=['Icke Coaches']).exists()


# @login_required
# @user_passes_test(is_coach)
class WorkoutListView(generic.ListView):
    model = Workout
    template_name = 'workout_list.html'
    context_object_name = 'workout_list'


# @login_required
# @user_passes_test(is_coach)
class WorkoutDetailView(generic.DetailView):
    model = Workout
    template_name = 'workout_detail.html'
    context_object_name = 'workout'


# @login_required
# @user_passes_test(is_coach)
def coaches(request):
    context = {
    }
    return render(request, 'coaches.html', context=context)


class NewWorkoutView(generic.FormView):
    template_name = 'edit_workout.html'
    form_class = WorkoutForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


def calendar(request):
    context = {
    }
    return render(request, 'calendar.html', context=context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


