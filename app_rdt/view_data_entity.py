import json, traceback
import datetime
from datetime import datetime, date
from .models import tempTBLSubmitConfig, productMaster, configViewTxCriteria, rdtDssRdtParamMstr, configViewTxResult, tempTBLVLDEntityLog, RdtEntityElementMaster, RdtEntityMaster
from . import connect_adb
from web_rdt_project.logger import writeLog
from django.http import JsonResponse
from django.core import serializers
from django.db import connection
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

RC_PER_PAGE = int(settings.VIEW_TX_RC_PER_PAGE)
CHUNK_SIZE = int(settings.VIEW_TX_CHUNK_SIZE)

def getEntityGroup(request)->dict:
    try:
        writeLog(request, 'In progress', 'getEntityGroup')
        dic = {}
        ls_entity_group = []
        qs_entity_group = RdtEntityMaster.objects.values('entity_group').order_by('entity_group_seq').distinct()
        for count, data in enumerate(qs_entity_group):
            ls_entity_group.append(data.get('entity_group'))
            dic["Data_Entity_Group"] = ls_entity_group
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getEntityGroup')
    return dic
    
def getEntityName(request)->dict:
    try:
        writeLog(request, 'In progress', 'getEntityName')
        dic = {}
        ls_entity_group = []
        ls_entity_name = []
        ls_bot_abbr = []
        qs_entity_name = RdtEntityMaster.objects.values('entity_group', 'entity_name', 'BOT_ABBR').order_by('entity_group_seq', 'entity_name_seq').distinct()
        for count, data in enumerate(qs_entity_name):
            ls_entity_group.append(data.get('entity_group'))
            ls_entity_name.append(data.get('entity_name'))
            ls_bot_abbr.append(data.get('BOT_ABBR'))
            dic["Data_Entity_Group"] = ls_entity_group
            dic["Data_Entity_Name"] = ls_entity_name
            dic["BOT_ABBR"] = ls_bot_abbr
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getEntityName')
    return dic

def getProduct(request):
    try:
        writeLog(request, 'In progress', 'getProduct')
        qs_product_master = productMaster.objects.values('product_code', 'product_name')
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getProduct')
    return qs_product_master

def getFrequency(request)->dict:
    try:
        writeLog(request, 'In progress', 'getFrequency')
        dic = {}
        ls_frequency = []
        ls_bot_abbr = []
        ls_model_abbr = []
        ls_entity_group_sj = []
        qs_frequency = RdtEntityMaster.objects.values('frequency', 'BOT_ABBR', 'MODEL_ABBR', 'entity_group_sj')
        for count, data in enumerate(qs_frequency):
            ls_frequency.append(data.get('frequency'))
            ls_bot_abbr.append(data.get('BOT_ABBR'))
            ls_model_abbr.append(data.get('MODEL_ABBR'))
            ls_entity_group_sj.append(data.get('entity_group_sj'))
            dic["Frequency"] = ls_frequency
            dic["BOT_ABBR"] = ls_bot_abbr
            dic["MODEL_ABBR"] = ls_model_abbr
            dic["entity_group_sj"] = ls_entity_group_sj
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getFrequency')
    return dic

def getEntityCriteria(request)->dict:
    try:
        writeLog(request, 'In progress', 'getEntityCriteria')
        dic = {}
        ls_bot_abbr = []
        ls_elm_name = []
        ls_elm_desc = []
        ls_criteria_require_flag = []
        ls_elm_type = []
        ls_elm_size = []
        ls_classification = []
        ls_elm_seq = []
        qs_criteria = configViewTxCriteria.objects.values('entity_elm__BOT_ABBR', 'entity_elm__elm_name', 'entity_elm__elm_desc', 'criteria_require_flag', 'entity_elm__elm_type', 'entity_elm__elm_size', 'entity_elm__classification', 'entity_elm__elm_seq').order_by('criteria_seq')
        for count, data in enumerate(qs_criteria):
            bot_abbr = data.get('entity_elm__BOT_ABBR')
            elm_name = data.get('entity_elm__elm_name')
            elm_desc = data.get('entity_elm__elm_desc')
            criteria_require_flag = data.get('criteria_require_flag')
            elm_type = data.get('entity_elm__elm_type')
            elm_size = data.get('entity_elm__elm_size')
            classification = data.get('entity_elm__classification')
            elm_seq = data.get('entity_elm__elm_seq')
            ls_bot_abbr.append(bot_abbr)
            ls_elm_name.append(elm_name)
            ls_elm_desc.append(elm_desc)
            ls_criteria_require_flag.append(criteria_require_flag)
            ls_elm_type.append(elm_type)
            ls_elm_size.append(elm_size)
            ls_classification.append(classification)
            ls_elm_seq.append(elm_seq)
        dic['BOT_ABBR'] = ls_bot_abbr
        dic['elm_name'] = ls_elm_name
        dic['elm_desc'] = ls_elm_desc
        dic['criteria_require_flag'] = ls_criteria_require_flag
        dic['elm_type'] = ls_elm_type
        dic['elm_size'] = ls_elm_size
        dic['classification'] = ls_classification
        dic['elm_seq'] = ls_elm_seq
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getEntityCriteria')
    return dic

def getClassification(request)->dict:
    try:
        writeLog(request, 'In progress', 'getClassification')
        dic = {}
        ls_param_nm = []
        ls_param_cd = []
        ls_param_val = []
        qs_classification = rdtDssRdtParamMstr.objects.values('param_nm', 'param_cd', 'param_val').distinct()
        for count, data in enumerate(qs_classification):
            ls_param_nm.append(data.get('param_nm'))
            ls_param_cd.append(data.get('param_cd'))
            ls_param_val.append(data.get('param_val'))
            dic["param_nm"] = ls_param_nm
            dic["param_cd"] = ls_param_cd
            dic["param_val"] = ls_param_val
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getClassification')
    return dic

def generateRawQuery(request, obj: dict, bot_abbr: str, model_abbr: str, entity_group_sj: str, condition: str)->str:
    try:
        writeLog(request, 'In progress', 'generateRawQuery')
        qs_result = configViewTxResult.objects.filter(entity_elm__BOT_ABBR=bot_abbr).values('entity_elm__BOT_ABBR', 'entity_elm__elm_name', 'entity_elm__elm_desc', 'entity_elm__require_flag', 'entity_elm__elm_type', 'entity_elm__elm_size', 'entity_elm__classification', 'entity_elm__elm_seq').order_by('result_seq')
        fields = ''
        raw_query = ''
        elm_name = ''
        from_con = ' FROM '
        where_cause = 'WHERE '
        convert_str = ''
        bsns_dt = str(obj.get('bsns_dt'))
        where_cause += 'bsns_dt' + '=' + "'" + bsns_dt + "'" + ' AND '
        if(condition == 'getConfigResult'):
            fields = 'WITH tempquery AS (SELECT row_number() over (order by ETL_KEY, BSNS_DT) as row, '
        else:
            fields = 'SELECT count(*) '
        for count, data in enumerate(qs_result):
            elm_name = data.get('entity_elm__elm_name')
            elm_type = data.get('entity_elm__elm_type')
            if(condition == 'getConfigResult'):
                fields += elm_name + ','
            for key, value in obj.items():
                if(key == elm_name and value != ''):
                    if(elm_type != 'classification'):
                        if(elm_type != 'date'):
                            where_cause += elm_name + '=' + "'" + value + "'" + ' AND '
                    else:
                        if(value != [''] and value != []):
                            convert_str = str(value)
                            convert_str = convert_str.replace('[','(')
                            convert_str = convert_str.replace(']',')')
                            where_cause += elm_name + ' IN ' + convert_str + ' AND '
        from_con += 'rdtdev' + '_modelhotfix_' + entity_group_sj + '_db.' + model_abbr + ' '+ where_cause[0:-5]
        raw_query += fields[0:-1] + from_con
        return raw_query
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'generateRawQuery')
    

def getConfigResult(request, _start: str, _length: str, page_number: int, ts: str)->dict:
    try:
        writeLog(request, 'In progress', 'getConfigResult')
        dic_job = {}
        entity_fields = request.POST.get('entity_fields', None)
        bot_abbr = request.POST.get('bot_abbr', None)
        product = request.POST.get('product', None)
        model_abbr = request.POST.get('model_abbr', None)
        entity_group_sj = request.POST.get('entity_group_sj', None)
        obj = json.loads(entity_fields)
        qs_result = configViewTxResult.objects.filter(entity_elm__BOT_ABBR=bot_abbr).values('entity_elm__BOT_ABBR', 'entity_elm__elm_name', 'entity_elm__elm_desc', 'entity_elm__require_flag', 'entity_elm__elm_type', 'entity_elm__elm_size', 'entity_elm__classification', 'entity_elm__elm_seq').order_by('result_seq')
        fields = 'WITH tempquery AS (SELECT row_number() over (order by ETL_KEY, BSNS_DT) as row,  '
        elm_name = ''
        from_con = ' FROM '
        where_cause = 'WHERE '
        convert_str = ''
        raw_query_unique = ''
        bsns_dt = str(obj.get('bsns_dt'))
        where_cause += 'bsns_dt' + '=' + "'" + bsns_dt + "'" + ' AND '
        raw_query_unique = generateRawQuery(request, obj, bot_abbr, model_abbr, entity_group_sj, "getConfigResult")
        start_row = int(_start)+1
        end_row = int(_start) + int(CHUNK_SIZE)
        raw_query_unique += ')' + 'SELECT * FROM tempquery WHERE row >= ' + str(start_row) + ' AND row <= ' + str(end_row)
        json_data = connect_adb.getCriteriaData(request, raw_query_unique, page_number, ts)
        writeLog(request, 'Success', 'getConfigResult')
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getConfigResult')
    return json_data

def getValidationStatus(request)->json:
    try:
        if request.method == 'POST':
            writeLog(request, 'In progress', 'getValidationStatus')
            entity_fields = request.POST.get('entity_fields', None)
            bot_abbr = request.POST.get('bot_abbr', None)
            model_abbr = request.POST.get('model_abbr', None)
            obj = json.loads(entity_fields)
            dic_job = {}
            dt_to_date = ''
            bsns_dt = str(obj.get('bsns_dt'))
            qs_tbl_vld_entity_log = tempTBLVLDEntityLog.objects.filter(vld_tbl_nm=model_abbr.upper(), bsns_dt=bsns_dt, actv_flag='Y').values('job_sts', 'entity_end_dttm')
            for data in qs_tbl_vld_entity_log:
                dic_job["job_sts"] = data.get('job_sts')
                dt_to_date = data.get('entity_end_dttm').date()
                dic_job["entity_end_dttm"] = dt_to_date
            writeLog(request, 'Success', 'getValidationStatus')
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getValidationStatus')
    return JsonResponse(dic_job,safe=False)

def getTotalRecord(request)->json:
    try:
        if request.method == 'POST':
            writeLog(request, 'In progress', 'getTotalRecord')
            entity_fields = request.POST.get('entity_fields', None)
            model_abbr = request.POST.get('model_abbr', None)
            entity_group_sj = request.POST.get('entity_group_sj', None)
            raw_query_unique = ''
            record = 0
            bot_abbr = request.POST.get('bot_abbr', None)
            obj = json.loads(entity_fields)
            raw_query_unique = generateRawQuery(request, obj, bot_abbr, model_abbr, entity_group_sj, 'getTotalRecord')
            record = connect_adb.getTotalRecordData(request, raw_query_unique)
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getTotalRecord')
    return JsonResponse(record,safe=False)

def getDatafromCache(request)->json:
    try:
        if request.method == 'POST':
            _start = request.POST.get('start')
            time_stamp = request.POST.get('time_stamp')
            _length = RC_PER_PAGE
            page_number = (int(_start)//int(_length)) + 1
            user_id = request.user.id
            cache_prefix = str(user_id) + '_' + str(time_stamp)
            print("time stamp: ", cache_prefix)
            print('Start local cache:{0} cache_prefix: {1}'.format(str(timezone.now()), cache_prefix))
            cache_key = cache_prefix + '_' + str(page_number)
            print('cache_key:',cache_key)
            test_cache_obj = cache.get(cache_key)

            if test_cache_obj is None:
                print('no cache')
                test_cache_obj = getConfigResult(request, _start, _length, page_number, cache_prefix)
            else:
                print('cache ready')
                print('start get cache with range', timezone.now())
                print('end get cache with range', timezone.now())
            

            total = len(test_cache_obj)
            response = {
                'data': test_cache_obj,
                'recordsTotal': total,
                'pageLength': RC_PER_PAGE,
            }
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'testGetAll')
    print('Stop local cache:{0} cache_prefix: {1}'.format(str( timezone.now()), cache_prefix))
    return JsonResponse(response,safe=False)

def getViewTxResult(request)->json:
    try:
        qs_data = configViewTxResult.objects.values("entity_elm_id"
        ,"entity_elm__BOT_ABBR"
        ,"entity_elm__elm_name"
        ,"entity_elm__elm_desc"
        ,"entity_elm__elm_desc_th"
        ,"entity_elm__elm_seq"
        ,"entity_elm__elm_key"
        ,"entity_elm__require_flag"
        ,"entity_elm__elm_type"
        ,"entity_elm__elm_size"
        ,"entity_elm__classification"
        ,"entity_elm__bot_elm_flag"
        ,"entity_elm__last_upd_date"
        ,"entity_elm__last_upd_by_id"
        ,"view_tx_result_id"
        ,"result_seq"
        ,"visible_flag"
        ,"ajm_link_flag"
        ,"ajm_allow_flag"
        ,"last_upd_date"
        ,"last_upd_by_id").order_by('entity_elm__BOT_ABBR', 'result_seq')
        result_json = json.dumps(list(qs_data), cls=DjangoJSONEncoder)
        return result_json

    except Exception as err:
        return {"error": str(err)}
