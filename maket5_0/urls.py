from django.urls import path
from . import views
from .views import LogStatusView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'maketVue'

urlpatterns = [

    # Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('accounts/log_status/', LogStatusView.as_view(), name='log_status'),
    path('settings/structure/', views.dictionary_settings, name='structure'),
    path('settings/fields/', views.fields_structure, name='fields_structure'),

    # Dictionary
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
    path('hex_from_pantone/<str:pantone>', views.hex_from_pantone, name='hex_from_pantone'),

    # Order
    path('order/<int:id_no>/<str:order>/<str:search_string>/<int:sh_deleted>',
         views.show_orders, name='orders'),
    path('delete_order/<int:order_no>', views.delete_order, name='delete_order'),
    path('reset_order/<int:order_id>', views.reset_order, name='reset_order'),
    path('import_file', views.import_file, name='import_order'),
    path('fix_order_errors', views.fix_order_errors, name='fix_order_errors'),

    # Additional Files
    path('additional_file/<int:order_pk>', views.additional_files_list, name='additional_files'),
    path('import_additional_file/<int:order_pk>', views.import_additional_file, name='import_additional_file'),
    path('additional_file_show/<int:file_pk>/<str:file_name>', views.additional_file_show, name='additional_file_show'),
    path('delete_additional_file/<int:file_no>', views.delete_additional_file, name='delete_additional_file'),
    path('reconnect_additional_file/<int:file_no>/<int:order_pk>', views.reconnect_additional_file,
         name='reconnect_additional_file'),
    path('files_additional_file/<int:id_no>/<str:search_string>/<int:sh_undeleted>',
         views.files_additional_file, name='files_additional_file'),
    path('files_additional_file_delete/<int:file_id>',
         views.files_additional_file_delete, name='files_additional_file_delete'),
    path('files_additional_file_delete_all',
         views.files_additional_file_delete_all, name='files_additional_file_delete_all'),

    # Patterns
    path('pattern_show/<int:file_pk>/<str:file_name>', views.pattern_show, name='pattern_show'),
    path('files_pattern/<int:id_no>/<str:search_string>/<int:sh_undeleted>',
         views.files_pattern, name='files_pattern'),
    path('files_pattern_delete/<int:file_id>',
         views.files_pattern_delete, name='files_pattern_delete'),
    path('files_pattern_delete_all',
         views.files_pattern_delete_all, name='files_pattern_delete_all'),

    # Maket
    path('maket_to_order/<int:order_no>', views.maket_to_order, name='maket_to_order'),
    path('maket_info/<int:maket_id>/<int:order_id>', views.maket_info, name='maket_info'),
    path('maket_grouping_change', views.maket_grouping_change, name='maket_grouping_change'),
    path('item_color_code_list/<str:article>', views.item_color_code_list, name='item_color_code_list'),
    path('maket_save', views.maket_save, name='maket_save'),
    path('maket_list/<str:search_string>/<int:sh_deleted>/<int:id_no>', views.maket_list_info, name='maket_list'),
    path('maket_delete/<int:maket_id>', views.maket_delete, name='maket_delete'),
    path('maket_restore/<int:maket_id>', views.maket_restore, name='maket_restore'),
    path('maket_file_save/<int:maket_id>', views.maket_file_save, name='maket_fil8%e_save'),
    path('maket_show/<int:maket_id>', views.maket_show, name='maket_show'),

    # Film
    path('film_list_for_group/<int:group_id>/<int:connected>', views.film_list_for_group, name='film_list_for_group'),
    path('group_to_film/<int:group_id>/<int:film_id>', views.group_to_film, name='group_to_film'),
    path('group_from_film/<int:group_id>/<int:film_id>', views.group_from_film, name='group_from_film'),
    path('film_list/<str:search_string>/<int:sh_deleted>/<int:id_no>', views.film_list_info, name='film_list'),
    path('toggle_film_status/<int:film_id>', views.toggle_film_status, name='toggle_film_status'),
    path('set_film_comment/<int:film_id>', views.set_film_comment, name='set_film_comment'),
    path('film_group_to_film/<int:group_id>/<int:film_id>', views.film_group_to_film, name='film_group_to_film'),
    path('film_group_from_film/<int:group_id>/<int:film_id>', views.film_group_from_film, name='film_group_from_film'),
    path('film_delete/<int:film_id>', views.film_delete, name='film_delete'),
    path('film_update/<int:film_id>', views.film_update, name='film_update'),
    path('film_file_save/<int:film_id>', views.film_file_save, name='film_file_save'),
    path('film_load/<int:film_id>', views.film_load, name='film_load'),
    path('maket_group_list_not_in_film',views.maket_group_list_not_in_film, name='maket_group_list_not_in_film'),
    path('film_update_with_list/<int:film_id>', views.film_update_with_list, name='film_update_with_list'),
]
