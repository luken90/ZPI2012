from django.conf.urls.defaults import *
from sklep.models import Towary, Klienci
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_reset

urlpatterns = patterns('',
    url(r'^produkty/$', 'django.views.generic.list_detail.object_list', {'queryset': Towary.objects.all().select_related('kategorie'), 'paginate_by': 3}, "sklep_produkty"),
    url(r'^kontakt/$', 'sklep.views.strona_kontakt', name="sklep_kontakt"),
    url(r'^index/$', 'sklep.views.koszyk', name="sklep_koszyk"),
    url(r'^menage/$', 'sklep.views.manage_articles', name="sklep_manage_articles"),
    url(r'^koszyk/$', 'sklep.views.koszykobsluga', name="koszykobsluga"),
    url(r'^klient/(\d+)/$', 'sklep.views.zmien_klienta', name="zmien_klienta"),
    url(r'^klient/$', 'sklep.views.dodaj_klienta', name="dodaj_klienta"),
    url(r'^rejestracja/$', 'sklep.views.register', name="sklep_register"),
    url(r'^logowanie/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^koszyk/dodaj/(\d+)/$', 'sklep.views.koszyk_dodaj', name="sklep_koszyk_dodaj"),
    url(r'^koszyk/usun/(\d+)/$', 'sklep.views.koszyk_usun', name="sklep_koszyk_usun"),
    url(r'^produkty/(\d+)/$', 'sklep.views.produkty_z_kategorii', name="sklep_kategoria"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/sklep/'} ),
    url(r'^password/reset/$', 'sklep.views.password_reset', {'template_name': 'registration/password_reset_form1.html','post_reset_redirect' : '/sklep/password/reset/done/'}),
    url(r'^password/reset/done/$', 'sklep.views.password_reset_done', {'template_name': 'registration/password_reset_done1.html'}),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'registration/password_reset_confirm1.html','post_reset_redirect' : '/sklep/password/done/'}),
    url(r'^password/done/$', 'django.contrib.auth.views.password_reset_complete',{'template_name': 'registration/password_reset_complete1.html'}),
    url(r'^setlang/(?P<lang_code>.*)/$', 'sklep.views.set_language'),
    url(r'', 'sklep.views.strona_glowna', name="sklep_glowna"),

    )
