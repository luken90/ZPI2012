﻿from django.conf.urls.defaults import *
from sklep.models import Towary

urlpatterns = patterns('',
    url(r'^produkty/$', 'django.views.generic.list_detail.object_list', {'queryset': Towary.objects.all().select_related('kategorie'), 'paginate_by': 1}, "sklep_produkty"),
)