from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q, Count
from .models import AuthPermission
from django.http import JsonResponse
import json
from django.core import serializers
from django.utils import timezone

def userPermission(request):
   
    qs = request.user.groups.all()
    data = json.loads(serializers.serialize("json", qs))
    
    permission_no_list = [ p['fields']['permissions'] for p in data]
    permission_no_list=list(set([item for sublist in permission_no_list for item in sublist]))

    permission_list = list(AuthPermission.objects.filter(id__in=permission_no_list).values_list('codename', flat=True))

    return permission_list

def checkuserPermission(request,permission):
    
    qs = request.user.groups.all()
    data = json.loads(serializers.serialize("json", qs))
    
    permission_no_list = [ p['fields']['permissions'] for p in data]
    permission_no_list=list(set([item for sublist in permission_no_list for item in sublist]))

    permission_list = list(AuthPermission.objects.filter(id__in=permission_no_list).values_list('codename', flat=True))

    if permission in permission_list : return True
    else : return False

