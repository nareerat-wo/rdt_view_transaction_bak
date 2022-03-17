import traceback, json
from . import connector
from web_rdt_project.logger import writeLog
from web_rdt_project.logger import my_handler
from django.conf import settings
from .models import rdtDssRdtParamMstr
from datetime import datetime
from django.utils import timezone
import json, os, pyodbc
from threading import Thread
from django.core.cache import cache
RC_PER_PAGE = int(settings.VIEW_TX_RC_PER_PAGE)
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

def getCriteriaData(request, query, page_number, cache_prefix):
    try:
        # print('Start Process ADB:', timezone.now())
        writeLog(request, 'In progress', 'getCriteriaData')
        print('Start ADB generateConnection', timezone.now())
        conn = connector.generateConnection()
        print('stop ADB generateConnection', timezone.now())
        print('Start ADB conn.cursor()', timezone.now())
        cursor = conn.cursor()
        print('Stop ADB conn.cursor()', timezone.now())
        # print('Start cursor.execute(query): ', timezone.now())
        # query += ' LIMIT 100'
        # print(query)
        # cursor.execute(query)
        # aemtest start ADB to dataframe
        #print('Start execute ADB', timezone.now())
        #print('Start execute ADB query:', query)
        #cursor.execute(query)
        #print('stop execute ADB', timezone.now())
        #print('Start execute ADB result fetch all:', timezone.now())
        #query_results = cursor.fetchall()
        #print('stop execute ADB result fetch all', timezone.now())
        #print('Start query to dataframe', timezone.now())
        #df = pd.DataFrame(query_results)
        #print('Stop query to dataframe', timezone.now())
        #print(df[:10])
        # aemtest end ADB to dataframe

        # aemtest start ADB to dataframe
        
        print('ADB query:', query)
        print('Start execute ADB:{0} cache_prefix: {1}'.format(str(timezone.now()), cache_prefix))
        cursor.execute(query)
        print('stop execute ADB:{0} cache_prefix: {1}'.format(str( timezone.now()), cache_prefix))
        print('Start record per first page', timezone.now())
        print('Start row_headers:', timezone.now())
        row_headers = [x[0] for x in cursor.description]
        print(type(row_headers))
        print(row_headers)
        print('End row_headers:', timezone.now())
        json_data = []
        index=0
        cache_key = cache_prefix + '_'
        for result in cursor:
            index=index+1
            json_data.append(dict(zip(row_headers,result)))
            if index==RC_PER_PAGE:
                cache.set(cache_key+str(page_number), json_data)
                break
        print('stop  record per first page', timezone.now())
        print('Start thread add cahce perpage:', timezone.now())
        t = Thread(target=create_cache_pages, args=(request, cursor, page_number+1, cache_prefix))
        t.start()
        print('stop execute ADB result fetch all', timezone.now())
        # print('json_data first page:', json_data)
        # aemtest end ADB to dataframe
        # print('End cursor.execute(query):', timezone.now())
        # print('Start row_headers:', timezone.now())
        # row_headers = [x[0] for x in cursor.description]
        # print(type(row_headers))
        # print(row_headers)
        # print('End row_headers:', timezone.now())
        # json_data = []
        # print('Start Process ADB fill to json: ', timezone.now())
        # for result in cursor:
        #     json_data.append(dict(zip(row_headers,result)))
        # print('Stop Process ADB fill to json: ', timezone.now())

    except Exception as error:
        print(error)
        writeLog(request, traceback.format_exc(), 'getCriteriaData')
    # print('End Process ADB:', timezone.now())
    return json_data

def create_cache_pages(request, cursor, page_number, cache_prefix):
    print('Start create_cache_pages:{0} cache_prefix: {1}'.format(str( timezone.now()), cache_prefix))
    print('create_cache_pages Start row_headers :', timezone.now())
    row_headers = [x[0] for x in cursor.description]
    print(type(row_headers))
    print(row_headers)
    print('create_cache_pages End row_headers:', timezone.now())
    page=page_number
    json_data = []
    index=0
    cache_key = cache_prefix + '_'
    # print('aem test len cursor2:', len(list(cursor)))
    for result in cursor:      
        index=index+1
        json_data.append(dict(zip(row_headers,result)))
        if index==RC_PER_PAGE:
            # print('create_cache_pages Start cache.set:', timezone.now())
            cache.set(cache_key+str(page), json_data)
            # print('cache_key:',cache_key+str(page))
            # print('create_cache_pages end cache.set:', timezone.now())
            json_data = []
            index=0
            page=page+1
            continue
    print('End create_cache_pages:{0} cache_prefix: {1}'.format(str( timezone.now()), cache_prefix))

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
    