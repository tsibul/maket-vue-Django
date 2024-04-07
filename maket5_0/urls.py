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
    path('settings/structure/', views.dictionary_settings, name='structure'),
    path('settings/fields/', views.fields_structure, name='fields_structure'),

    path('dictionary_data/<str:dict_type>/<int:id_no>/<str:order>/<str:search_string>/<int:sh_deleted>',
         views.dictionary_records, name='dictionary_records'),
    path('dictionary_filter/<str:dict_type>/<str:filter_dictionary>/<int:filter_dictionary_id>',
         views.dictionary_filter, name='dictionary_json_filter'),
    path('dictionary_record/<str:dict_type>/<int:record_id>',
         views.dictionary_single_record, name='dictionary_record'),
    path('dictionary_update/<str:dict_type>',
         views.dictionary_update, name='dictionary_update'),
    path('dictionary_delete/<str:dict_type>/<int:record_id>',
         views.dictionary_delete, name='dictionary_delete'),

    path('order/<int:id_no>/<str:order>/<str:search_string>/<int:sh_deleted>',
         views.show_orders, name='orders'),
    path('import_order', views.import_order, name='import_order'),
    path('delete_order/<int:order_no>', views.delete_order, name='delete_order'),

]
