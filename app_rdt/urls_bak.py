from django.urls import path
#from .views import (
#    PostListView,
#    PostDetailView,
#    PostCreateView,
#    PostUpdateView,
#    PostDeleteView,
#    UserPostListView
#)
from . import views

urlpatterns = [
    path('', views.homepage, name='web-home'),
    path('userPermission', views.userPermission, name='home-userpermission'),
   #path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
   #path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
   #path('post/new/', PostCreateView.as_view(), name='post-create'),
   #path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
   #path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
   path('dashboard/reconciliation', views.dashboard_reconciliation, name='dashboard-reconciliation'),
   path('dashboard/userPermission', views.userPermission, name='dashboard-userpermission'),
   path('submitBOT/approval', views.submitBOT_submission, name='submitBOT-submission'),
   path('submitBOT/userPermission', views.userPermission, name='submitBOT-userpermission'),
   path('submitBOT/approvalresult', views.submitBOT_entitystatus, name='submitBOT-entitystatus'),
   path('dataEntity/view', views.viewDataEntity, name='dataEntity-view'),
   path('dataEntity/get_config_result', views.get_config_result, name='getConfigResult'),
   path('dataEntity/get_description', views.get_description, name='getDescription'),
   path('dataEntity/get_name_list', views.get_name_list, name='getNameList'),
   path('dataEntity/get_validation_status', views.get_validation_status, name='getValidationStatus'),
   path('dataEntity/get_total_record', views.get_total_record, name='getTotalRecord'),
#    path('dataEntity/get_entity_group', views.get_entity_group, name='get_entity_group'),
#    path('dataEntity/get_entity_name', views.get_entity_name, name='get_entity_name')
#    path('dataEntity/get_product', views.get_product, name='get_product'),
]