from django.urls import path

from appointment.views import AddAppointmentView, LoadTimeslots, ViewAppointment, DeleteAppointmentView, AddRoomView, \
    SearchRoom, ViewRooms, AdmitPatientView, ViewAdmitPatient

urlpatterns = [
    path('search_timeslot/', LoadTimeslots.as_view(), name='search_timeslot'),
    path('add_appointment/', AddAppointmentView.as_view(), name='add_appointment'),
    path('view_appointment/', ViewAppointment.as_view(), name='view_appointment'),
    path('delete_appointment/<int:id>/', DeleteAppointmentView.as_view(), name='delete_appointment'),
    path('add_rooms/', AddRoomView.as_view(), name='add_rooms'),
    path('search_room/', SearchRoom.as_view(), name='search_room'),
    path('view_rooms/', ViewRooms.as_view(), name='view_rooms'),
    path('admit_patient/', AdmitPatientView.as_view(), name='admit_patient'),
    path('view_admit_patient/', ViewAdmitPatient.as_view(), name='view_admit_patient'),

]
