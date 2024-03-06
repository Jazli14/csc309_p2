from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, Contact
# from .models import Calendar

# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Fields Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'user_type',
                ),
            },
        ),
    )

admin.site.register(UserAccount, CustomUserAdmin)
admin.site.register(Contact)
# admin.site.register(Calendar)
