import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .client import MicrosoftClient
from .models import MicrosoftAccount, MicrosoftGroup
from .utils import get_hook

from django.http import JsonResponse
import json
from django.core import serializers
from web_rdt_project.logger import writeLog_signin

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger("django")
User = get_user_model()


class MicrosoftAuthenticationBackend(ModelBackend):
    """ Authentication backend to authenticate a user against their Microsoft
        Uses Microsoft's Graph OAuth to authentiate. """

    config = None
    microsoft = None

    def __init__(self, user=None):
        from .conf import config

        self.config = config

    def authenticate(self, request, code=None):
        """
            Authenticates the user against the Django backend
                using a Microsoft auth code from
            https://login.microsoftonline.com/common/oauth2/v2.0/authorize or
            https://login.live.com/oauth20_authorize.srf

            For more details:
            https://developer.microsoft.com/en-us/graph/docs/get-started/rest
        """

        self.microsoft = MicrosoftClient(request=request)

        user = None
        if code is not None:
            # fetch OAuth token
            token = self.microsoft.fetch_token(code=code)
            
            # validate permission scopes
            if "access_token" in token and self.microsoft.valid_scopes(
                token["scope"]
            ):
                user = self._authenticate_user(request)

        if user is not None:
            self._call_hook(user)

        return user

    def _authenticate_user(self,request):
        return self._authenticate_microsoft_user(request)

    def _authenticate_microsoft_user(self, request):
        claims = self.microsoft.get_claims()

        writeLog_signin(request, 'Success', claims, 'Login Success')
        
        if claims is not None:
            return self._get_user_from_microsoft(claims)

        return None

    def _get_user_from_microsoft(self, data):
        """ Retrieves existing Django user """
        user = None
        microsoft_user = self._get_microsoft_user(data)

        if microsoft_user is not None:
            user = self._verify_microsoft_user(microsoft_user, data)

        return user

    def _get_microsoft_user(self, data):
        microsoft_user = None

        try:
            microsoft_user = MicrosoftAccount.objects.get(
                microsoft_id=data["sub"]
            )
        except MicrosoftAccount.DoesNotExist:
            if self.config.MICROSOFT_AUTH_AUTO_CREATE:
                # create new Microsoft Account
                microsoft_user = MicrosoftAccount(microsoft_id=data["sub"])
                microsoft_user.save()

        return microsoft_user

    def _verify_microsoft_user(self, microsoft_user, data):
        user = microsoft_user.user

        if user is None:
            fullname = data.get("name")
            first_name, last_name = "", ""
            if fullname is not None:
                first_name, last_name = data["name"].split(" ", 1)

            try:
                # create new Django user from provided data
                user = User.objects.get(email=data["preferred_username"])

                if user.first_name == "" and user.last_name == "":
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
            except User.DoesNotExist:
                user = User(
                    username=data["preferred_username"][:150],
                    first_name=first_name,
                    last_name=last_name,
                    email=data["preferred_username"],
                )
                user.save()

            existing_account = self._get_existing_microsoft_account(user)
            if existing_account is not None:
                if self.config.MICROSOFT_AUTH_AUTO_REPLACE_ACCOUNTS:
                    existing_account.user = None
                    existing_account.save()
                else:
                    logger.warning(
                        (
                            "User {} already has linked Microsoft "
                            "account and MICROSOFT_AUTH_AUTO_REPLACE_ACCOUNTS "
                            "is False"
                        ).format(user.email)
                    )
                    return None

            microsoft_user.user = user
            microsoft_user.save()

        #custom
        existing_group = self._get_existing_microsoft_group(microsoft_user.user_id,data["groups"])

        return user

    #custom
    def _get_existing_microsoft_group(self, user, groups):

        user = User.objects.get(id=user)

        aad_groups = MicrosoftGroup.objects.filter(aad_group_id__in=groups).values('group')
        current_groups = user.groups.all().values('id')

        if aad_groups is not None:
            for_del = list(current_groups.difference(aad_groups).values_list('id', flat=True))

            if for_del is not None:
                for ids in for_del:
                    user.groups.remove(ids)

            for_add = list(aad_groups.difference(current_groups).values_list('group', flat=True))

            if for_add is not None:
                for ids in for_add:
                    user.groups.add(ids)

        elif current_groups is not None:
            user.groups.clear()

        return None

    def _get_existing_microsoft_account(self, user):
        try:
            return MicrosoftAccount.objects.get(user=user)
        except MicrosoftAccount.DoesNotExist:
            return None

    def _call_hook(self, user):
        function = get_hook("MICROSOFT_AUTH_AUTHENTICATE_HOOK")
        if function is not None:
            function(user, self.microsoft.token)
