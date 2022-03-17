from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from django.db.models import Q, Count
#from .models import (
#    Post, 
#)
from django.http import JsonResponse
import json
from django.core import serializers
from datetime import datetime
from django.utils import timezone
from web_rdt_project.logger import writeLog
from web_rdt_project.logger import my_handler
import csv, io, sys, traceback
from . import web_config
from . import base
from threading import Thread
from . import multisite_config
from .models import DataReadiness
from . import view_data_entity, connect_adb, schedules

#get web version
web_version = getattr(web_config, "web_version", None)
print("web_version:",web_version)
# schedules.backend_schedulejob()
schedules.backend_schedulejob()

def userPermission(request):
    if request.method == 'POST':
        data = base.userPermission(request) 
    return JsonResponse(data,safe=False)

@login_required
def homepage(request):
    try:
        #get multisite config
        multiSite_announcement = multisite_config.getMultiSiteInfo("announcement")
        multiSite_home_page = multisite_config.getMultiSiteInfo("home_page")
        context = {
            'web_version': web_version, 
            'title': 'Home',
            'announcement':multiSite_announcement 
         }
        return render(request, 'web/'+multiSite_home_page , context)
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'homepage')   

#class PostListView(LoginRequiredMixin,ListView):
#    model = Post
#    template_name = 'web/home.html'
#    context_object_name = 'posts'
#    ordering = ['-date_posted']
#    paginate_by = 3
#
#class UserPostListView(ListView):
#    model = Post
#    template_name = 'web/user_posts.html'
#    context_object_name = 'posts'
#    ordering = ['-date_posted']
#    paginate_by = 3
#
#    def get_queryset(self):
#        user = get_object_or_404(User, username=self.kwargs.get('username'))
#        return Post.objects.filter(author=user).order_by('-date_posted')
#
#
#class PostDetailView(DetailView):
#    model = Post
#    template_name = 'web/post_detail.html'
#
#class PostCreateView(LoginRequiredMixin, CreateView):
#    model = Post
#    fields = ['title', 'content']
#    template_name = 'web/post_form.html'
#
#    def form_valid(self, form):
#        form.instance.author = self.request.user
#        return super().form_valid(form)
#
#class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#    model = Post
#    fields = ['title', 'content']
#    template_name = 'web/post_form.html'
#
#    def form_valid(self, form):
#        form.instance.author = self.request.user
#        return super().form_valid(form)
#
#    def test_func(self):
#        post = self.get_object()
#        if self.request.user == post.author:
#            return True
#        return False
#
#class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#    model = Post
#    template_name = 'web/post_confirm_delete.html'
#    success_url = '/'
#
#    def test_func(self):
#        post = self.get_object()
#        if self.request.user == post.author:
#            return True
#        return False

@login_required
def dashboard_reconciliation(request):
    context = {
            'web_version': web_version, 
            'title': 'reconciliation',
            'submenu': True
        }
    return render(request, 'web/dashboard_reconciliation.html')

@login_required
def submitBOT_submission(request):
    context = {
            'web_version': web_version, 
            'title': 'approvalBOT',
            'submenu': True
        }
    return render(request, 'web/approvalBOT_approval2.html')

# @login_required
# def submitBOT_entitystatus(request):
#     #aem test
#     #obj_DataReadiness = DataReadiness.objects.raw('SELECT area, table_name, data_date, data_volumn FROM aims_config_db.data_readiness')
#     #ds_DataReadinessobj_DataReadiness = obj_DataReadiness.objects.all()
#     #print('aem test ds_DataReadiness:', list(ds_DataReadiness))
#     #print('aemtest start:', timezone.now())
#     #for p in DataReadiness.objects.raw('SELECT * FROM aims_config_db.data_readiness'):
#     #    print('aem test  p area:', p.area)
#     #    print('aem test  p: data_volumn', p.data_volumn)
# #
#     #print('aemtest end:', timezone.now())
# #
#     #from django.db import connections
#     #with connections['dbrick_db'].cursor() as cursor:
#     #    #cursor.execute("INSERT INTO aims_config_db.data_readiness VALUES('aem test2', 'aem test table', '3', '4', '5')")
#     #    #cursor.execute("UPDATE aims_config_db.data_readiness SET data_volumn='6' WHERE area='aem test'")
#     #    cursor.execute("DELETE FROM aims_config_db.data_readiness WHERE area='aem test'")
#     #    cursor.execute("SELECT * FROM aims_config_db.data_readiness")
#     #    row = cursor.fetchone()
#     #    print('aem test  insert row:',list(row))
#     #aem test 
#     context = {
#             'web_version': web_version, 
#             'title': 'approvalBOTresult',
#             'submenu': True
#         }
#     return render(request, 'web/approvalBOT_approvalresult2.html')


@login_required
def viewDataEntity(request):
    try:
        qs_entity_group = json.dumps(view_data_entity.getEntityGroup(request))
        qs_entity_name = json.dumps(view_data_entity.getEntityName(request))
        qs_product_master = view_data_entity.getProduct(request)
        qs_frequency = json.dumps(view_data_entity.getFrequency(request))
        qs_criteria = json.dumps(view_data_entity.getEntityCriteria(request))
        qs_classification = json.dumps(view_data_entity.getClassification(request))
        qs_view_tx_result = view_data_entity.getViewTxResult(request)
        context = {
            'web_version': web_version, 
            'title': 'Data Entity',
            'submenu': 'View Data Entity',
            'entity_group': qs_entity_group,
            'entity_name': qs_entity_name,
            'product_master': qs_product_master,
            'frequency_bot_abbr': qs_frequency,
            'criteria': qs_criteria,
            'classification': qs_classification,
            'view_tx_result': qs_view_tx_result
        }
        return render(request, 'web/view_data_entity.html' , context)
    except Exception as error:
        writeLog(request, traceback.format_exc(), 'view_data_entity')