from django.urls import path
from . import views
from .views import LogStatusView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'marketing_report'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('accounts/log_status/', LogStatusView.as_view(), name='log_status'),

    # path('', views.index, name='index'),
    #
    # path('report/', views.reports, name='reports'),
    # path('json_report/<int:report_no>/<str:report_type>/<str:period>/<str:date_begin>/<str:date_end>/<str:argument>',
    #      views.json_periods, name='json_report'),
    #
    # path('customer/', views.customer, name='customer'),
    #
    #
    # path('dictionary/', views.dictionary, name='dictionary'),
    # path('dictionary_last_id/<str:dict_type>', views.dictionary_last_id, name='dictionary_last_id'),
    # path('dict_update/<str:dict_type>', views.dictionary_update, name='dictionary_update'),
    # path('dict_delete/<str:dict_type>/<int:id_no>', views.dictionary_delete, name='dictionary_delete'),
    # path('json_dict_next_20/<str:dict_type>/<int:id_no>/<str:order>/<str:search_string>/<int:sh_deleted>', views.dictionary_json,
    #      name='dictionary_json'),
    # path('dictionary_json_filter/<str:dict_type>/<str:filter_dictionary>/<int:filter_dictionary_id>',
    #      views.dictionary_json_filter, name='dictionary_json_filter'),
    #
    # path('imports/', views.imports, name='imports'),
    # path('import_file/', views.import_file, name='import_file'),
    # path('edit_temporary_base/', views.edit_temporary_base, name='edit_temporary_base'),
    # path('import_new_customers/', views.customers_new_to_main_db, name='import_new_customers'),
    # path('import_changed_customers/', views.customer_change_to_customer, name='import_changed_customers'),
    # path('first_last_sales_dates/', views.first_last_sales_dates, name='first_last_sales_dates'),
    #
    # path('reassign_periods/', views.reassign_report_periods, name='reassign_periods'),
    #
    # path('admin/', views.admin, name='admin_site'),
    # path('customer_export/', views.customer_export, name='customer_export'),
    # path('goods_export/', views.goods_export, name='goods_export'),
    # path('customer_group_json/', views.customer_group_json, name='customer_group_json'),
    #
    # path('report/<str:report_class>/<str:report_type>/<str:period>/<str:parameter>/<int:begin>/<int:end>',
    #      views.json_report, name='report_json'),

]
