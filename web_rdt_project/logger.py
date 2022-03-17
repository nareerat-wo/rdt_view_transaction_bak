import os,logging,socket,datetime,random
from django.conf import settings
from django.db.models.signals import pre_save, post_save 
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
from django.contrib.sites.models import Site
from app_rdt.models import (
    RdtLog
)
#=============================================================================
hostname = socket.gethostname()
server_source_address = socket.gethostbyname(hostname) 
RDT_APP_ENV_DIR = os.environ.get('RDT_APP_ENV_DIR')
current_site = Site.objects.get_current()
server_source_hostname = current_site.domain
#=============================================================================
def writeLog(request, status, eventType, **kwargs):
    now = datetime.datetime.now()
    if(settings.RDT_CONFIG_CUSTOM_WRITE_LOG == True):
        if(eventType == 'inquiry_getInquiryResult_execute' and status == 'Success'):
            message = str(kwargs)
            message = message.strip('{')
            message = message.replace("'execute_type':","")
            message = message.replace(" 'event_type': ","'")
            message = message.replace("}","'")
            message = message.replace(" ","")
        elif(eventType == 'campaign_save'):
            message = str(kwargs)
        elif(status == 'Inprocess'):
            message = str(kwargs)
        else:
            message = ''
        if(request != ""):
            get_cliect_ip = visitor_ip_address(request)
            sessionid = request.COOKIES['sessionid']
            username = str(request.user.username)
            user_id = str(request.user.id)
        elif(request == ""):
            sessionid = ''
            username = ''
            get_cliect_ip = ''
            user_id = None
        if ((status != 'In progress' and status != 'Success') and status != 'Inprocess'):
            status = ('Error :'+str(status))
        filename = now.strftime(RDT_APP_ENV_DIR+'log_file/RDT_log_all_%d-%m-%Y.log')
        logging.basicConfig(filename=filename)
        logger = logging.getLogger('')
        logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d|RDT|'+eventType+'|'+get_cliect_ip+'||'+username+'||'+server_source_address+'|'+server_source_hostname+'|||'+status+'|'+message+'|'+str(sessionid),'%d/%m/%Y %H:%M:%S')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.debug(eventType+':Logging in progress...')
        logger.removeHandler(fileHandler)
        # rdtLogging(now,"adt_log",eventType,get_cliect_ip,None,username,status,message,str(sessionid),user_id)
        return


@receiver(post_save, sender=LogEntry)
def my_handler(sender, instance, **kwargs):
    now = datetime.datetime.now()
    if(settings.RDT_ADMIN_WRITE_LOG == True):
        instance_date = str(instance.action_time)
        instance_date = datetime.datetime.strptime(instance_date, '%Y-%m-%d %H:%M:%S.%f')
        instance_date = instance_date.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        if(str(instance.change_message) != ""):
            change_message = str(instance.change_message)
        elif(str(instance.change_message) == ""):
            change_message = '-'
        filename = now.strftime(RDT_APP_ENV_DIR+'log_file/admin_log_file/RDT_log_admin_%d-%m-%Y.log.')
        logging.basicConfig(filename=filename)
        logger = logging.getLogger('RDT')
        logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler(filename)
        formatter = logging.Formatter(str(instance_date)+'|%(name)s|'+str(instance.content_type)+'|||'+str(instance.user)+'||'+server_source_address+'|'+server_source_hostname+'||||'+str(instance)+'|'+change_message,'%d/%m/%Y %H:%M:%S')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.debug('ADMIN LOGGING')
        logger.removeHandler(fileHandler)
        # rdtLogging(now,"rdt_admin_log",str(instance),None,None,str(instance.user),None,change_message,None,str(instance.user.id))
        return

def rdtLogging(datetime,log_type,event_type,clientIP,clientHostname,username,status,message,other,user_id):
    log = RdtLog()
    log.transaction_datetime = datetime
    log.log_type = log_type
    log.application_name = "rdt"
    log.event_type = event_type
    log.source_address = clientIP
    log.source_hostname = clientHostname
    log.source_user = username
    log.source_object = None
    log.destination_address = server_source_address
    log.destination_hostname = server_source_hostname
    log.destination_user = None
    log.destination_object = None
    if status != None:
        if str(status) == "In progress" or str(status) == "Success":
            log.status = status
        elif str(status) == "Inprocess":
            log.status = status
        else:
            log.status = status[:5]
            log.remark = status[:4000]
    else:
        log.status = None
        log.remark = None
    log.message = message[:2000]
    log.other = other
    log.last_upd_date = datetime
    log.last_upd_by_id = user_id
    log.save()
    return

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def writeLog_signin(request, status, cliams_aad, message):
    now = datetime.datetime.now()
    if(settings.RDT_SIGNIN_WRITE_LOG == True):
        if(cliams_aad): 
            client_ip = cliams_aad['ipaddr']
            rdt_server_hostname = str(request.get_host())
            client_username = cliams_aad['preferred_username']
            
            filename = now.strftime(RDT_APP_ENV_DIR+'log_file/signin_log_file/RDT_log_signin_%d-%m-%Y.log')
            logging.basicConfig(filename=filename)
            logger = logging.getLogger('')
            logger.setLevel(logging.DEBUG)
            fileHandler = logging.FileHandler(filename)

            formatter = logging.Formatter('%(asctime)-.19s|RDT|Login|'+client_ip+'|'+server_source_hostname+'|'+client_username+'|||'+server_source_address+'|'+rdt_server_hostname+'||||'+status+'|'+message)
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
            logger.debug('Login:Logging in progress...')
            logger.removeHandler(fileHandler)
            get_cliect_ip = visitor_ip_address(request)
            # rdtLogging(now,"rdt_log_signin","Login",get_cliect_ip,None,client_username,status,message,None,None)