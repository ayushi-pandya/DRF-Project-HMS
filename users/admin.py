from django.contrib import admin
from users.models import User, UserRole, StaffSpeciality, Staff
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'username', 'email', 'phone', 'age', 'address', 'gender', 'role', 'profile', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'age', 'address', 'gender', 'role', 'profile',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone', 'age', 'address', 'gender', 'role', 'password1', 'password2', 'profile'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username', 'id')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(UserRole)
admin.site.register(StaffSpeciality)
admin.site.register(Staff)

