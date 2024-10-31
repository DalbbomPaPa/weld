from django.contrib import admin

from .models import Weld_info, Weld_raw_data

class raw_data_admin(admin.ModelAdmin):
  date_hierarchy = 'date'

admin.site.register(Weld_info)
admin.site.register(Weld_raw_data, raw_data_admin)