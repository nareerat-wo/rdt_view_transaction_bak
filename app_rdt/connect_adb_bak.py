import traceback, json
from . import connector
from web_rdt_project.logger import writeLog
from web_rdt_project.logger import my_handler
from .models import rdtDssRdtParamMstr
from datetime import datetime
from django.utils import timezone
import json, os, pyodbc

def getDataAdb():
    try:
        dic = {}
        ls_data = []
        table_name = "rdtdev_persist_dss_db.dss_rdt_param_mstr"
        conn = connector.generateConnection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE bsns_dt = (SELECT max(bsns_dt) FROM {table_name})")

        rdtDssRdtParamMstr.objects.all().delete()

        for row in cursor.fetchall():
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
            insert_data = rdtDssRdtParamMstr(param_nm=row[0], param_cd=row[1], param_val=row[2],  param_desc=row[3],  src_sys=row[4],  src_val=row[5],  src_col=row[6],  src_desc=row[7],  optn=row[8],  rec_load_ts=row[9],  job_nm=row[10], bsns_dt=row[11])
            ls_data.append(insert_data)
            print(row[1])
        rdtDssRdtParamMstr.objects.bulk_create(ls_data)
        print('end time:', timezone.now())
        
    except Exception as error:
        print(error)
    return 'test'

def getCriteriaData(request, query):
    try:
        print('Start Process ADB:', timezone.now())
        writeLog(request, 'In progress', 'getCriteriaData')
        conn = connector.generateConnection()
        cursor = conn.cursor()
        print('Start cursor.execute(query): ', timezone.now())
        cursor.execute(query)
        print('End cursor.execute(query):', timezone.now())
        print('Start row_headers:', timezone.now())
        row_headers = [x[0] for x in cursor.description]
        print(type(row_headers))
        print(row_headers)
        print('End row_headers:', timezone.now())
        json_data = []
        print('Start Process ADB fill to json: ', timezone.now())
        for result in cursor:
            json_data.append(dict(zip(row_headers,result)))
        print('Stop Process ADB fill to json: ', timezone.now())

    except Exception as error:
        print(error)
        writeLog(request, traceback.format_exc(), 'getCriteriaData')
    print('End Process ADB:', timezone.now())
    return json_data

def getTotalRecordData(request, query):
    try:
        print('Start Process ADB total record:', timezone.now())
        writeLog(request, 'In progress', 'getTotalRecordData')
        conn = connector.generateConnection()
        cursor = conn.cursor()
        print('Start cursor.execute(query): ', timezone.now())
        cursor.execute(query)
        print('End cursor.execute(query):', timezone.now())
        result=cursor.fetchone()
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getTotalRecordData')
    print('End Process ADB total record:', timezone.now())
    return result[0]
    