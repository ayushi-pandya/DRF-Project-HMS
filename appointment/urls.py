from django.urls import path

from appointment.views import AddAppointmentView, LoadTimeslots, ViewAppointment

urlpatterns = [
    path('search_timeslot/', LoadTimeslots.as_view(), name='search_timeslot'),
    path('add_appointment/', AddAppointmentView.as_view(), name='add_appointment'),
    path('view_appointment/', ViewAppointment.as_view(), name='view_appointment'),

]
