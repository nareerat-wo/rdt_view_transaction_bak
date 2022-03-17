import json, traceback
import datetime
from datetime import datetime, date
from .models import tempTBLSubmitConfig, productMaster, configViewTxCriteria, rdtDssRdtParamMstr, configViewTxResult, tempTBLVLDEntityLog
from . import connect_adb
from web_rdt_project.logger import writeLog
from django.http import JsonResponse
from django.core import serializers
from django.db import connection
from django.utils import timezone

def getEntityGroup(request):
    try:
        writeLog(request, 'In progress', 'getEntityGroup')
        dic = {}
        ls_entity_group = []
        cursor = connection.cursor()
        cursor.execute("SELECT distinct data_entity_group, cast(SUBSTRING(Data_Entity_Name, 1, CHARINDEX('.', Data_Entity_Name)-1) as int) as seq_entity_group FROM rdt_config_dev_stg.temp_TBL_SUBMIT_CONFIG ORDER BY seq_entity_group")
        for row in cursor.fetchall():
            ls_entity_group.append(row[0])
            dic["Data_Entity_Group"] = ls_entity_group
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getEntityGroup')
    return dic
    
def getEntityName(request):
    try:
        writeLog(request, 'In progress', 'getEntityName')
        dic = {}
        ls_entity_group = []
        ls_entity_name = []
        ls_bot_abbr = []
        cursor = connection.cursor()
        cursor.execute("SELECT distinct data_entity_group ,Data_Entity_Name ,[BOT_ABBR] ,cast(SUBSTRING(Data_Entity_Name, 1, CHARINDEX('.', Data_Entity_Name)-1) as int) as seq_entity_group ,cast(SUBSTRING(Data_Entity_Name, CHARINDEX('.', Data_Entity_Name)+1, 2) as int) as seq_entity_name FROM rdt_config_dev_stg.temp_TBL_SUBMIT_CONFIG ORDER BY seq_entity_group, seq_entity_name")
        for row in cursor.fetchall():
            ls_entity_group.append(row[0])
            ls_entity_name.append(row[1])
            ls_bot_abbr.append(row[2])
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

def getFrequency(request):
    try:
        writeLog(request, 'In progress', 'getFrequency')
        dic = {}
        ls_frequency = []
        ls_bot_abbr = []
        qs_frequency = tempTBLSubmitConfig.objects.values('Frequency', 'BOT_ABBR')
        for count, data in enumerate(qs_frequency):
            ls_frequency.append(data.get('Frequency'))
            ls_bot_abbr.append(data.get('BOT_ABBR'))
            dic["Frequency"] = ls_frequency
            dic["BOT_ABBR"] = ls_bot_abbr
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getFrequency')
    return dic

def getEntityCriteria(request):
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
        dic['bot_abbr'] = ls_bot_abbr
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

def getClassification(request):
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
        # print(dic)
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getClassification')
    return dic

def getConfigResult(request):
    try:
        print('Start Process SSMS:', timezone.now())
        writeLog(request, 'In progress', 'getConfigResult')
        _start = request.POST.get('start')
        _length = request.POST.get('length')
        dic_job = {}
        entity_fields = request.POST.get('entity_fields', None)
        bot_abbr = request.POST.get('bot_abbr', None)
        product = request.POST.get('product', None)
        obj = json.loads(entity_fields)
        qs_result = configViewTxResult.objects.filter(entity_elm__BOT_ABBR=bot_abbr).values('entity_elm__BOT_ABBR', 'entity_elm__elm_name', 'entity_elm__elm_desc', 'entity_elm__require_flag', 'entity_elm__elm_type', 'entity_elm__elm_size', 'entity_elm__classification', 'entity_elm__elm_seq').order_by('result_seq')
        qs_tbl_submit_config = tempTBLSubmitConfig.objects.filter(BOT_ABBR=bot_abbr, Frequency=obj['frequency']).values('MODEL_ABBR')
        fields = 'WITH tempquery AS (SELECT row_number() over (order by ETL_KEY, BSNS_DT) as count,  '
        elm_name = ''
        from_con = ' FROM '
        where_cause = 'WHERE '
        convert_str = ''
        raw_query = ''
        model_abbr = ''
        bsns_dt_convert = datetime.strptime(obj.get('bsns_dt'), "%d-%m-%Y").strftime("%Y-%m-%d")
        fields += 'etl_key'+ ','+ 'bsns_dt' + ','
        where_cause += 'bsns_dt' + '=' + "'" + bsns_dt_convert + "'" + ' AND '
        for count, data in enumerate(qs_result):
            elm_name = data.get('entity_elm__elm_name')
            elm_type = data.get('entity_elm__elm_type')
            fields += elm_name + ','
            for key, value in obj.items():
                if(key == elm_name and value != ''):
                    if(elm_type != 'classification'):
                        if(elm_type != 'date'):
                            where_cause += elm_name + '=' + "'" + value + "'" + ' AND '
                        # if(elm_type == 'datetime'):
                        #     date_convert = datetime.strptime(value, '%d-%m-%Y').date()
                        #     date_convert_combine =  datetime.combine(date_convert, datetime.min.time())
                        #     where_cause += elm_name + '=' + "'" + str(date_convert_combine) + "'" + ' AND '
                        # else:
                        #     # fields += elm_name + ','
                        #     where_cause += elm_name + '=' + "'" + value + "'" + ' AND '
                    else:
                        if(value != [''] and value != []):
                            convert_str = str(value)
                            convert_str = convert_str.replace('[','(')
                            convert_str = convert_str.replace(']',')')
                            fields += elm_name + ','
                            where_cause += elm_name + ' IN ' + convert_str + ' AND '
        start_row = int(_start)+1
        end_row = start_row + int(_length)-1
        for data in qs_tbl_submit_config:
            from_con += 'rdtdev_modelhotfix_cnprty_db.' + data.get('MODEL_ABBR') + ' '+ where_cause[0:-5] + ')' + 'SELECT * FROM tempquery WHERE count >= ' + str(start_row) + ' AND count <= ' + str(end_row)
            model_abbr = data.get('MODEL_ABBR')
        raw_query += fields[0:-1] + from_con
        print("raw_query: {}", raw_query)
        json_data = connect_adb.getCriteriaData(request, raw_query)
        total = len(json_data)
        response = {
            'data': json_data,
            'recordsTotal': total,
            'pageLength': 20,
        }
        writeLog(request, 'Success', 'getConfigResult')
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getConfigResult')
    print('End Process SSMS:', timezone.now())
    return response

def getNameList(request):
    try:
        print('Start Process getNameList: ', timezone.now())
        writeLog(request, 'In progress', 'getNameList')
        bot_abbr = request.POST.get('bot_abbr', None)
        dic = {}
        ls_elm_name = []
        ls_elm_desc = []
        elm_name = ''
        elm_desc = ''
        ls_elm_name.append('count')
        ls_elm_name.append('bsns_dt')
        ls_elm_desc.append('')
        ls_elm_desc.append('bsns_dt')
        qs_result = configViewTxResult.objects.filter(entity_elm__BOT_ABBR=bot_abbr).values('entity_elm__elm_name', 'entity_elm__elm_desc').order_by('result_seq')
        for count, data in enumerate(qs_result):
            elm_name = data.get('entity_elm__elm_name')
            elm_desc = data.get('entity_elm__elm_desc')
            ls_elm_name.append(elm_name)
            ls_elm_desc.append(elm_desc)
        dic['elm_name'] = ls_elm_name
        dic['elm_desc'] = ls_elm_desc
        writeLog(request, 'Success', 'getDescription')
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getNameList')
    print('Stop Process getNameList: ', timezone.now())
    return dic

def getDescription(request):
    try:
        print('Start Process getDescription: ', timezone.now())
        writeLog(request, 'In progress', 'getDescription')
        bot_abbr = request.POST.get('bot_abbr', None)
        dic_elm_desc = {}
        ls_elm_desc = []
        ls_elm_name = []
        elm_desc = ''
        elm_name = ''
        ls_elm_name.append('count')
        ls_elm_name.append('bsns_dt')
        ls_elm_desc.append('')
        ls_elm_desc.append('bsns_dt')
        qs_result_desc = configViewTxResult.objects.filter(entity_elm__BOT_ABBR=bot_abbr).values('entity_elm__elm_name', 'entity_elm__elm_desc').order_by('result_seq')
        for count, data in enumerate(qs_result_desc):
            elm_name = data.get('entity_elm__elm_name')
            elm_desc = data.get('entity_elm__elm_desc')
            ls_elm_name.append(elm_name)
            ls_elm_desc.append(elm_desc)
        dic_elm_desc['elm_name'] = ls_elm_name
        dic_elm_desc['elm_desc'] = ls_elm_desc
        writeLog(request, 'Success', 'getDescription')
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getDescription')
    print('Stop Process getDescription: ', timezone.now())
    return dic_elm_desc

def getValidationStatus(request):
    try:
        print('Start Process getValidationStatus: ', timezone.now())
        writeLog(request, 'In progress', 'getValidationStatus')
        entity_fields = request.POST.get('entity_fields', None)
        bot_abbr = request.POST.get('bot_abbr', None)
        obj = json.loads(entity_fields)
        dic_job = {}
        dt_to_date = ''
        model_abbr= ''
        writeLog(request, 'In progress', 'getValidationStatus')
        qs_tbl_submit_config = tempTBLSubmitConfig.objects.filter(BOT_ABBR=bot_abbr, Frequency=obj['frequency']).values('MODEL_ABBR')
        bsns_dt_convert = datetime.strptime(obj.get('bsns_dt'), "%d-%m-%Y").strftime("%Y-%m-%d")
        for data in qs_tbl_submit_config:
            model_abbr = data.get('MODEL_ABBR')
        print("model_abbr: {}", (model_abbr.upper()))
        print("bsns_dt_convert: {}",(bsns_dt_convert))
        qs_tbl_vld_entity_log = tempTBLVLDEntityLog.objects.filter(vld_tbl_nm=model_abbr.upper(), bsns_dt=bsns_dt_convert, actv_flag='Y').values('job_sts', 'entity_end_dttm')
        for data in qs_tbl_vld_entity_log:
            dic_job["job_sts"] = data.get('job_sts')
            dt_to_date = data.get('entity_end_dttm').date()
            dic_job["entity_end_dttm"] = dt_to_date
        writeLog(request, 'Success', 'getValidationStatus')
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'getValidationStatus')
    print('Stop Process getValidationStatus: ', timezone.now())
    return dic_job

def getTotalRecord(request):
    try:
        print('Start Process getTotalRecord: ', timezone.now())
        writeLog(request, 'In progress', 'getTotalRecord')
        entity_fields = request.POST.get('entity_fields', None)
        raw_query = ''
        record = 0
        field = 'SELECT count(*) '
        from_con = 'FROM '
        bot_abbr = request.POST.get('bot_abbr', None)
        obj = json.loads(entity_fields)
        qs_tbl_submit_config = tempTBLSubmitConfig.objects.filter(BOT_ABBR=bot_abbr, Frequency=obj['frequency']).values('MODEL_ABBR')
        for data in qs_tbl_submit_config:
            from_con += 'rdtdev_modelhotfix_cnprty_db.' + data.get('MODEL_ABBR')
        raw_query += field + from_con
        record = connect_adb.getTotalRecordData(request, raw_query)
    except:
        writeLog(request, traceback.format_exc(), 'getTotalRecord')
    return record
    
