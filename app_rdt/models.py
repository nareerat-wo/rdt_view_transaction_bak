from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

RDT_CONFIG_DB_SCHEMA = ''
if settings.RDT_CONFIG_DB_SCHEMA and len(settings.RDT_CONFIG_DB_SCHEMA) > 0:
    RDT_CONFIG_DB_SCHEMA = settings.RDT_CONFIG_DB_SCHEMA
    print('RDT_CONFIG_DB_SCHEMA:', RDT_CONFIG_DB_SCHEMA)

########## General Model ##########
#class Post(models.Model):
#    title = models.CharField(max_length=100)
#    content = models.TextField()
#    date_posted = models.DateTimeField(default=timezone.now)
#    author = models.ForeignKey(User, on_delete=models.CASCADE)
#
#    def get_absolute_url(self):
#        return reverse('post-detail', kwargs={'pk': self.pk})
#    class Meta:
#        managed = False
#        app_label = 'app360'
#        db_table = AIMS_CONFIG_DB_SCHEMA + '].[app360_post'  

########## Custom Permission Model ##########
class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    # content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        app_label = 'app360'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[auth_permission'
        unique_together = (('codename'),)

class RdtLog(models.Model):
    transaction_datetime = models.DateTimeField()
    log_type = models.CharField(max_length=100, blank=True, null=True)
    application_name = models.CharField(max_length=100, blank=True, null=True)
    event_type = models.CharField(max_length=200, blank=True, null=True)
    source_address = models.CharField(max_length=200, blank=True, null=True)
    source_hostname = models.CharField(max_length=200, blank=True, null=True)
    source_user = models.CharField(max_length=200, blank=True, null=True)
    source_object = models.CharField(max_length=500, blank=True, null=True)
    destination_address = models.CharField(max_length=500, blank=True, null=True)
    destination_hostname = models.CharField(max_length=200, blank=True, null=True)
    destination_user = models.CharField(max_length=200, blank=True, null=True)
    destination_object = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=2000, blank=True, null=True)
    other = models.CharField(max_length=1024, blank=True, null=True)
    remark = models.CharField(max_length=4000, blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_log'
        
########## Home Page Model ##########    
class RdtAnnouncement(models.Model):
    subject = models.CharField(max_length=1024, blank=True, null=True)
    content = models.CharField(max_length=2048, blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_announcement'



########## databrick Model ########## 
class DataReadiness(models.Model):
    area = models.CharField(max_length=255, blank=True, null=True, primary_key=True)
    table_name = models.CharField(max_length=255, blank=True, null=True)
    data_date = models.CharField(max_length=255, blank=True, null=True)
    data_volumn = models.CharField(max_length=255, blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False        
        app_label = 'databrick'
        db_table = 'data_readiness'

########## data entity view ##########
class RdtEntityElementMaster(models.Model):
    entity_elm_id = models.IntegerField(primary_key=True)
    BOT_ABBR = models.CharField(max_length=100)
    elm_name = models.CharField(max_length=100)
    elm_desc = models.CharField(max_length=100, blank=True, null=True)
    elm_desc_th = models.CharField(max_length=200, blank=True, null=True)
    elm_seq = models.IntegerField(blank=True, null=True)
    elm_key = models.CharField(max_length=10, blank=True, null=True)
    require_flag = models.CharField(max_length=1, blank=True, null=True)
    elm_type = models.CharField(max_length=20, blank=True, null=True)
    elm_size = models.IntegerField(blank=True, null=True)
    classification = models.CharField(max_length=100, blank=True, null=True)
    bot_elm_flag = models.CharField(max_length=1, blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_entity_element_master'

# class entityClassification(models.Model):
#     CLSFC_NM = models.CharField(max_length=100, blank=True, null=True)
#     CLSFC_CD = models.CharField(max_length=100, blank=True, null=True)
#     CLSFC_VAL = models.CharField(max_length=100, blank=True, null=True)
#     CLSFC_DESC = models.CharField(max_length=100, blank=True, null=True)
#     SRC_SYS = models.CharField(max_length=100, blank=True, null=True)
#     SRC_VAL = models.CharField(max_length=100, blank=True, null=True)
#     SRC_COL = models.CharField(max_length=100, blank=True, null=True)
#     SRC_DESC = models.CharField(max_length=100, blank=True, null=True)
#     JOB_NM = models.CharField(max_length=100, blank=True, null=True)
#     BSNS_DT = models.DateField(blank=True, null=True)
#     rec_load_ts = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         app_label = 'app_rdt'
#         db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_entity_classification'

class rdtDssRdtParamMstr(models.Model):
    param_nm = models.CharField(max_length=100)
    param_cd = models.CharField(max_length=100)
    param_val = models.CharField(max_length=100)
    param_desc = models.CharField(max_length=100, blank=True, null=True)
    src_sys = models.CharField(max_length=100)
    src_val = models.CharField(max_length=100)
    src_col = models.CharField(max_length=200, blank=True, null=True)
    src_desc = models.CharField(max_length=100, blank=True, null=True)
    optn = models.CharField(max_length=100, blank=True, null=True)
    rec_load_ts = models.DateTimeField(blank=True, null=True)
    job_nm = models.CharField(max_length=100, blank=True, null=True)
    bsns_dt = models.DateField()

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_dss_rdt_param_mstr'

class configViewTxCriteria(models.Model):
    view_tx_criteria_id = models.AutoField(primary_key=True)
    entity_elm = models.ForeignKey('RdtEntityElementMaster', models.DO_NOTHING)
    criteria_seq = models.IntegerField()
    criteria_require_flag = models.CharField(max_length=1, blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_config_view_tx_criteria'

class configViewTxResult(models.Model):
    view_tx_result_id = models.AutoField(primary_key=True)
    entity_elm = models.ForeignKey('RdtEntityElementMaster', models.DO_NOTHING)
    result_seq = models.IntegerField()
    visible_flag = models.CharField(max_length=1)
    ajm_link_flag = models.CharField(max_length=1)
    ajm_allow_flag = models.CharField(max_length=1)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_config_view_tx_result'

class productMaster(models.Model):
    product_code = models.CharField(primary_key=True, max_length=100)   
    product_name = models.CharField(max_length=100)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_product_master'

class productRdtCode(models.Model):
    product_rdtcode_id = models.IntegerField(blank=True, primary_key=True)
    product_id = models.IntegerField(blank=True)
    rdt_code = models.CharField(max_length=100, blank=True)
    original_code = models.CharField(max_length=100, blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_product_rdtcode'

class tempTBLVLDEntityLog(models.Model):
    job_nm = models.CharField(max_length=80)
    entity_nm = models.CharField(primary_key=True, max_length=80)
    bsns_dt = models.DateField()
    vld_tbl_nm = models.CharField(max_length=80)
    entity_strt_dttm = models.DateTimeField()
    entity_end_dttm = models.DateTimeField(blank=True, null=True)
    entity_grp = models.CharField(max_length=80, blank=True, null=True)
    batch_nm = models.CharField(max_length=100)
    actv_flag = models.CharField(max_length=1, blank=True, null=True)
    job_sts = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[tbl_vld_entity_log'
        unique_together = (('entity_nm', 'vld_tbl_nm', 'entity_strt_dttm'),)

class tempTBLSubmitConfig(models.Model):
    Data_Entity_Group = models.CharField(max_length=100, blank=True, primary_key=True)
    Data_Entity_Name = models.CharField(max_length=100, blank=True)
    BOT_ABBR = models.CharField(max_length=100, blank=True)
    MODEL_ABBR = models.CharField(max_length=100, blank=True, null=True)
    Frequency = models.CharField(max_length=100, blank=True, null=True)
    Submission_Type = models.CharField(max_length=100, blank=True, null=True)
    SLA_DAY = models.CharField(max_length=100, blank=True, null=True)
    Export_File_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[temp_TBL_SUBMIT_CONFIG'

class RdtEntityMaster(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity_group = models.CharField(max_length=50)
    entity_group_seq = models.IntegerField()
    entity_group_sj = models.CharField(max_length=20)
    entity_name = models.CharField(max_length=50)
    entity_name_seq = models.IntegerField()
    BOT_ABBR = models.CharField(max_length=20)
    MODEL_ABBR = models.CharField(max_length=20, blank=True, null=True)
    frequency = models.CharField(max_length=20, blank=True, null=True)
    submission_type = models.CharField(max_length=30, blank=True, null=True)
    sla_day = models.IntegerField(blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_entity_master'

class RdtScheduleExecute(models.Model):
    schedule_execute_id = models.AutoField(primary_key=True)
    schedule_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=256, blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'app_rdt'
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_schedule_execute'

class RdtProductContingent(models.Model):
    product_ctg_id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=20)
    ctg_type_code = models.CharField(max_length=20)
    original_ctg_type_code = models.CharField(max_length=20, blank=True, null=True)
    last_upd_date = models.DateTimeField(blank=True, null=True)
    last_upd_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = RDT_CONFIG_DB_SCHEMA + '].[rdt_product_contingent'