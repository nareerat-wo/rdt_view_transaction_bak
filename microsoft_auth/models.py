from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib import admin


class UnicodeSpaceUsernameValidator(UnicodeUsernameValidator):
    """ validator to allow spaces in username """

    regex = r"^[\w\.@+\- ]+$"


# replace UnicodeUsernameValidator on User model...
User = get_user_model()
for field in User._meta.fields:
    if field.name == "username":
        for index, validator in enumerate(field.validators):
            if isinstance(validator, UnicodeUsernameValidator):
                field.validators[index] = UnicodeSpaceUsernameValidator()


class MicrosoftAccount(models.Model):
    microsoft_id = models.CharField(_("microsoft account id"), max_length=64)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="microsoft_account",
    )

    def __str__(self):
        return self.microsoft_id


#Custom model
class MicrosoftGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    aad_group_id = models.CharField(max_length=100)

    def __str__(self):
        return self.group.name

class MicrosoftGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'aad_group_id')