from django.contrib import admin

from appointment.models import Appointments, Room, Admit, AdmitStaff, Notification

admin.site.register(Appointments)
admin.site.register(Room)
admin.site.register(Admit)
admin.site.register(AdmitStaff)
admin.site.register(Notification)
