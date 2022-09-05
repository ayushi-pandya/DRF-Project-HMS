from django.urls import path

from users.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, \
    SendPasswordResetEmailView, UserPasswordResetView, AddUserRoleView, AddStaffSpecialityView, UserDeleteView, \
    UserUpdateView, StaffUpdateView

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


]
