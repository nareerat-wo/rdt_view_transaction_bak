from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import RdtAnnouncement

admin.site.site_header = 'RDT administration'
admin.site.site_title = 'RDT administration'

admin.site.register(RdtAnnouncement)
