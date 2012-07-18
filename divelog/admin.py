from divelog.models import Dive, Sample
from django.contrib import admin

class DiveAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'size',
        'fingerprint',
        'max_depth',
        'date_time',
        'duration',
    )
    
class SampleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dive',
        'time',
        'depth',
        'temperature',
    )

admin.site.register(Dive, DiveAdmin)
admin.site.register(Sample, SampleAdmin)
