from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('',
    	views.index, 
    	name='index'
    	),
    path('whiteboard/',
    	views.WhiteboardView.as_view(),
    	name='whiteboard'
    	),
    path('coaches/',
    	views.coaches,
    	name='coaches'
    	),
    path('whiteboard/detail/<int:pk>',
    	views.TrainingPartInstanceDetailView.as_view(),
    	name='training-part-instance-detail'
    	),
    path('login/',
    	auth_views.LoginView.as_view()
    	),
    path('coaches/workout/<int:pk>', 
    	views.WorkoutDetailView.as_view(), 
    	name='workout-detail-view'
    	),
    path('coaches/workouts/', 
    	views.WorkoutListView.as_view(), 
    	name='workout-list-view'
    	),
   	path('coaches/workout/new', 
    	views.NewWorkoutView.as_view(), 
    	name='new-workout'
    	),
    path('coaches/calendar/', 
        views.calendar,
        name='calendar'
        ),
path(
    'admin/password_reset/',
    auth_views.PasswordResetView.as_view(),
    name='admin_password_reset',
),
path(
    'admin/password_reset/done/',
    auth_views.PasswordResetDoneView.as_view(),
    name='password_reset_done',
),
path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(),
    name='password_reset_confirm',
),
path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(),
    name='password_reset_complete',
),
path(
    'profile/',
    views.update_profile,
    name='profile',
),
] 