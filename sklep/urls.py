from django.conf.urls.defaults import *
from sklep.models import Towary

urlpatterns = patterns('',
    url(r'^produkty/$', 'django.views.generic.list_detail.object_list', {'queryset': Towary.objects.all().select_related('kategorie'), 'paginate_by': 3}, "sklep_produkty"),
	url(r'^koszyk/$', 'sklep.views.koszyk', name="sklep_koszyk"),
	url(r'^koszyk/dodaj/(\d+)/$', 'sklep.views.koszyk_dodaj', name="sklep_koszyk_dodaj"),
	url(r'^produkty/(\d+)/$', 'sklep.views.produkty_z_kategorii', name="sklep_kategoria"),
)