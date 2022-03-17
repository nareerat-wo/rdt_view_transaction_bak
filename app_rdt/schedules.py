from . import scheduler_services, connect_adb, connector
from .models import rdtDssRdtParamMstr, RdtScheduleExecute
from datetime import datetime
from django.utils import timezone
import json, os, pyodbc

misfire_grace_time_config = 60

def saveScheduleExecute(save_type, schedule_id, remark, schedule_last_upd_by):
    try:

        exe_date = timezone.now()
        if save_type == 'start':
            print(save_type)
            schedule_exe = RdtScheduleExecute()
            schedule_exe.schedule_id = schedule_id 
            schedule_exe.status = 'Started'
            schedule_exe.started = exe_date        
        else:
            schedule_exe = RdtScheduleExecute.objects.filter(schedule_id=schedule_id, status = 'Started').order_by('-last_upd_date')[0]
            schedule_exe.status = save_type
            schedule_exe.finished = exe_date
            schedule_exe.remark = remark
        schedule_exe.last_upd_date = exe_date
        schedule_exe.last_upd_by = schedule_last_upd_by
        schedule_exe.save()

    except Exception as error:
        # writeLog('', traceback.format_exc(), 'save_schedule_execute')
        print(error)

def getDataAdb():
    try:
        count = 0
        schedule_last_upd_by = 'schedule_job'
        saveScheduleExecute('start', 'getDataAdb', '', schedule_last_upd_by)
        print('start time:', timezone.now())
        dic = {}
        ls_data = []
        # print('test1')
        table_name = "rdtdev_persist_dss_db.dss_rdt_param_mstr"
        conn = connector.generateConnection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE bsns_dt = (SELECT max(bsns_dt) FROM {table_name})")
        # print('test_connect_adb')
        print(f"Query output: SELECT * FROM {table_name}\n")

        rdtDssRdtParamMstr.objects.all().delete()

        for row in cursor.fetchall():
            count += 1
            if(row[0]==None):
                row[0] = '-'
            if(row[1]==None):
                row[1] = '-'
            if(row[2]==None):
                row[2] = '-'
            if(row[4]==None):
                row[4] = '-'
            if(row[5]==None):
                row[5] = '-'
                # print(row[5])
            insert_data = rdtDssRdtParamMstr(param_nm=row[0], param_cd=row[1], param_val=row[2],  param_desc=row[3],  src_sys=row[4],  src_val=row[5],  src_col=row[6],  src_desc=row[7],  optn=row[8],  rec_load_ts=row[9],  job_nm=row[10], bsns_dt=row[11])
            # insert_data.save()
            ls_data.append(insert_data)
            print(row[1])
        rdtDssRdtParamMstr.objects.bulk_create(ls_data)
        # for data in ls_data:
        #     data.save()
        print(len(ls_data))
        print('end time:', timezone.now())
        remark = 'count: {}'.format(count)
        saveScheduleExecute('Success', 'getDataAdb', remark, schedule_last_upd_by)
        
    except Exception as error:
        print(error)

def backend_schedulejob():
    
    start_date = '2022-01-18'
    # start_date_mod = datetime.strptime(start_date, '%Y-%m-%d')
    
    # scheduler_services.scheduler.add_job(getDataAdb, 'cron', start_date= start_date, day_of_week='*', hour=13, minute=36, misfire_grace_time = misfire_grace_time_config, id = 'getDataAdb')
    #scheduler_services.scheduler.add_job(schedulejobs.schedulejob_campaign_upd_status_end, 'cron', start_date= start_date, day_of_week='*', hour=5, misfire_grace_time = misfire_grace_time_config, id = 'campaign_upd_status_end')

# start Back-end Process
backend_schedulejob()