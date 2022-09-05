from django.urls import path

from appointment.views import AddAppointmentView, LoadTimeslots

urlpatterns = [
    path('search_timeslot/', LoadTimeslots.as_view(), name='search_timeslot'),
    path('add_appointment/', AddAppointmentView.as_view(), name='add_appointment'),

]
