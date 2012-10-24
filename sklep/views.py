# Create your views here.
# coding: utf-8
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.core.mail import send_mail
from django.template import Context, loader
from django.conf import settings
from sklep.models import Towary, Kategorie
from sklep.forms import ZamowienieForm, TowarForm
from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.urlresolvers import reverse

def strona_glowna(request):
    koszyk = request.session.get('koszyk', [])
    #if koszyk:
    #    kontekst = {'koszyk': produkty, 'formularz': formularz}
    #else:
    kontekst = {'koszyk': []}
    
    return direct_to_template(request, 'sklep/glowna.html', extra_context = kontekst)
	
#def strona_kontakt(request):
#    koszyk = request.session.get('koszyk', [])
#    #if koszyk:
#    #    kontekst = {'koszyk': produkty, 'formularz': formularz}
#    #else:
#    kontekst = {'koszyk': []}
#    
#    return direct_to_template(request, 'sklep/kontakt.html', extra_context = kontekst)
def strona_kontakt(request):
    produkty = list(Towary.objects.filter(pk__in=2))
    if request.method == 'POST': # If the form has been submitted...
        form = TowarForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = TowarForm(instance=produkty) # An unbound form

    return TemplateResponse(request, 'sklep/kontakt.html', {'form': form})
	
    #return render(request, 'sklep/towary_list.html', {
    #    'form': form,
    #})
	
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
	

	
def produkty_z_kategorii(request, id_kategorii):
    kategoria1 = get_object_or_404(Kategorie, pk=int(id_kategorii))
    return object_list(
        request,
        queryset=Towary.objects.filter(kategoria=kategoria1).select_related('kategoria'),
        paginate_by=1,
        extra_context={'kategoria1': kategoria1}
    )