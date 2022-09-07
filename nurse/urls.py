from django.urls import path

from nurse.views import AssignDuty, SearchDuty, ViewDuty

urlpatterns = [
    path('assign_duty/', AssignDuty.as_view(), name='assign_duty'),
    path('view_duty/', ViewDuty.as_view(), name='view_duty'),
    path('search_duty/', SearchDuty.as_view(), name='search_duty'),

]
