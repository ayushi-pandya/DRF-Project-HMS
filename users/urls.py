from django.urls import path

from users.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, \
    SendPasswordResetEmailView, UserPasswordResetView, AddUserRoleView, AddStaffSpecialityView, UserDeleteView, \
    UserUpdateView, StaffUpdateView, SearchUser, ViewUser, SearchStaff, ViewStaff, AddMedicineView, PrescriptionView, \
    EmergencyCaseView, SearchEmergency, ViewEmergency, MedicineUpdateView, SearchMedicine, ViewMedicine, \
    ViewTodayAppointment, ViewPrescription, EnterFeedback, ViewFeedback

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('add_role/', AddUserRoleView.as_view(), name='add_role'),
    path('add_speciality/', AddStaffSpecialityView.as_view(), name='add_speciality'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('changepassword/', UserChangePasswordView.as_view(), name='change_password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send_reset_password_email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset_password'),
    path('update_user/<int:pk>/', UserUpdateView.as_view(), name='update_user'),
    path('update_staff/<int:id>/', StaffUpdateView.as_view(), name='update_staff'),
    path('delete_user/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('search_user/', SearchUser.as_view(), name='search_user'),
    path('view_user/', ViewUser.as_view(), name='view_user'),
    path('search_staff/', SearchStaff.as_view(), name='search_staff'),
    path('view_staff/', ViewStaff.as_view(), name='view_staff'),
    path('prescription/', PrescriptionView.as_view(), name='prescription'),
    path('view_prescription/', ViewPrescription.as_view(), name='view_prescription'),
    path('emergency_case/', EmergencyCaseView.as_view(), name='emergency_case'),
    path('view_emergency/', ViewEmergency.as_view(), name='view_emergency'),
    path('search_emergency/', SearchEmergency.as_view(), name='search_emergency'),
    path('add_medicine/', AddMedicineView.as_view(), name='add_medicine'),
    path('update_medicine/<int:id>/', MedicineUpdateView.as_view(), name='update_medicine'),
    path('search_medicine/', SearchMedicine.as_view(), name='search_medicine'),
    path('view_medicine/', ViewMedicine.as_view(), name='view_medicine'),
    path('view_todays_appointment/', ViewTodayAppointment.as_view(), name='view_todays_appointment'),
    path('feedback/', EnterFeedback.as_view(), name='feedback'),
    path('view_feedback/', ViewFeedback.as_view(), name='view_feedback'),

]
