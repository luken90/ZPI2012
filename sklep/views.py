# Create your views here.
# coding: utf-8
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.core.mail import send_mail
from django.template import Context, loader
from django.conf import settings
from sklep.models import Towary
from sklep.forms import ZamowienieForm

def koszyk(request):
    koszyk = request.session.get('koszyk', [])
    produkty = list(Towary.objects.filter(pk__in=koszyk))
    
    if request.method == 'POST':
        formularz = ZamowienieForm(request.POST)
        
        if formularz.is_valid():
            dane = formularz.cleaned_data
            tresc = loader.get_template('sklep/zamowienie.txt').render(Context({'produkty': produkty, 'dane': dane}))

            send_mail('Potwierdzenie zakupu', tresc, settings.EMAIL_SKLEPU, [dane['email']])
            send_mail(u'Zamowienie', tresc, dane['email'], [settings.EMAIL_SKLEPU])
            
            del request.session['koszyk']
            
            return HttpResponseRedirect(reverse('sklep_koszyk'))
    else:
        formularz = ZamowienieForm()
    
    if koszyk:
        kontekst = {'koszyk': produkty, 'formularz': formularz}
    else:
        kontekst = {'koszyk': []}
    
    return direct_to_template(request, 'sklep/koszyk.html', extra_context = kontekst)

def koszyk_dodaj(request, id_produktu):
    koszyk = request.session.get('koszyk', [])
    if int(id_produktu) not in koszyk:
        koszyk.append(int(id_produktu))
    request.session['koszyk'] = koszyk
    return HttpResponseRedirect(reverse('sklep_koszyk'))
