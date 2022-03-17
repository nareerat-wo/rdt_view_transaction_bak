from django.contrib.sites.models import Site
from .models import (
    RdtAnnouncement
)

def getMultiSiteInfo(datarequest):
    domain = Site.objects.get_current().domain
    announcement = RdtAnnouncement.objects.all().order_by('-last_upd_date')[:1]
    home_page='home.html'

    if datarequest == 'announcement': return announcement
    elif datarequest == 'home_page': return home_page
