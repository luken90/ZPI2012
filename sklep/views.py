# Create your views here.
# coding: utf-8
from django.http import Http404
from django import http 
from django.utils.translation import check_for_language 
from django.http import HttpResponseRedirect, HttpResponse,  HttpRequest
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.core.mail import send_mail
from django.template import Context, loader
from datetime import date
from django.conf import settings
from sklep.models import Towary, Kategorie, Klienci, Stanowiska, Zamowienia, OpisyZamowien, Pracownicy
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from sklep.forms import ZamowienieForm, TowarForm, KlienciForm, StanowiskaForm, ZamowieniaForm, OpisyZamowienForm, UserCreateForm, UserInfoForm, KlForm
from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.db.models import Max
from django.forms.formsets import formset_factory
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Klienci.objects.create(login=instance)
#
#post_save.connect(create_user_profile, sender=User)
def index(request):
    if request.method == 'POST':
        form = StanowiskaForm(request.POST)
        new_stanowiska = form.save()
    return render_to_response('sklep/index.html', context_instance=RequestContext(request))	

	
def set_language(request, lang_code): 
    """ 
    Patched for Get method 
    """ 
    next = request.REQUEST.get('next', None) 
    if not next: 
        next = 'sklep/glowna.html' 
    response = http.HttpResponseRedirect(next) 
    if lang_code and check_for_language(lang_code): 
        if hasattr(request, 'session'): 
            request.session['django_language'] = lang_code 
        else: 
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code) 
    return response 
	
def manage_articles(request):
    koszyk = request.session.get('koszyk', [])
    zmienna = 0
    #print zmienna
    produkty = list(Towary.objects.filter(pk__in=koszyk))
    liczba = Towary.objects.filter(pk__in=koszyk).count()
    OpisyZamowienFormSet = formset_factory(OpisyZamowienForm, extra = liczba)
    if request.method == 'POST':
        formset = OpisyZamowienFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for forA in formset:
                #print zmienna
                wartosc= produkty.__getitem__(zmienna)
                new_opis = forA.save(commit=False)
                new_opis.ident = -1
                #new_opis.ident = zam.idzamowienia
                #new_opis.idzamowienia1 = new_zamowienia
                new_opis.idtowaru = wartosc
                #new_opis.ilosc = forA.ilosc['k']
                #new_opis.ilosc = forA.ilosc
                zmienna+=1
                new_opis.save()
               
    else:
        formset = OpisyZamowienFormSet()
    return render_to_response('sklep/manage_articles.html', {'formset': formset}, context_instance=RequestContext(request))	
	
def koszykobsluga(request):
    koszyk = request.session.get('koszyk', [])
    produkty = list(Towary.objects.filter(pk__in=koszyk))
    liczba = Towary.objects.filter(pk__in=koszyk).count()	
    zmienna=0
    OpisyZamowienFormSet = formset_factory(OpisyZamowienForm, extra = liczba)
	
    if request.method == 'POST': # If the form has been submitted...
	klient = Klienci.objects.get(login=request.user.pk)
	pracownik = Pracownicy.objects.get(nazwisko='Sklep internetowy')
	
        form = ZamowieniaForm(request.POST) # A form bound to the POST data
        formset = OpisyZamowienFormSet(request.POST, request.FILES)# , initial=[{'ident': u'Article #1', 'idzamowienia1': u'Article #2','idtowaru': u'Article #3','ilosc': u'Article #4'},]
        if form.is_valid() and formset.is_valid(): # All validation rules pass
            zam=Zamowienia.objects.all().order_by('idzamowienia').reverse()[0]
            wynik=zam.idzamowienia
            new_zamowienia = form.save(commit=False)
            new_zamowienia.idzamowienia = wynik+1
            new_zamowienia.nik = klient
            new_zamowienia.np = pracownik
            new_zamowienia.data_zamowienia = date.today()
            new_zamowienia.status = 'Niezrealizowane'
            new_zamowienia.save()
            for forA in formset:
                wartosc= produkty.__getitem__(zmienna)
                new_opis = forA.save(commit=False)
                new_opis.ident = -1
                new_opis.idzamowienia1 = new_zamowienia
                new_opis.idtowaru = wartosc
                zmienna+=1
                new_opis.save()
            del request.session['koszyk']
            
            return HttpResponseRedirect(reverse('koszykobsluga'))
            #return HttpResponseRedirect('/sklep/') # Redirect after POST
    else:
        form = ZamowieniaForm()		
        formset = OpisyZamowienFormSet()
		
    if koszyk:
        kontekst = {'koszyk': produkty, 'form': form, 'formset': formset}
    else:
        kontekst = {'koszyk': []}
    return render_to_response('sklep/koszykobsluga.html',kontekst, context_instance=RequestContext(request))	
    #return direct_to_template(request, 'sklep/koszykobsluga.html', extra_context = kontekst)

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form1.html',
                   email_template_name='registration/password_reset_email1.html',
                   subject_template_name='registration/password_reset_subject1.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_done(request,
                        template_name='registration/password_reset_done1.html',
                        current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
                           template_name='registration/password_reset_confirm1.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
View that checks the hash in a password reset link and presents a
form for entering a new password.
"""
    UserModel = get_user_model()
    assert uidb36 is not None and token is not None # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
        user = UserModel.objects.get(id=uid_int)
    except (ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete1.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL)
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form1.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done1.html',
                         current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
	
def dodaj_klienta(request):
    if request.method == 'POST': # If the form has been submitted...
        form = KlienciForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            new_klienci = form.save(commit=False)
            #new_klienci.nik = form.nik
            #new_klienci.nip = form.nip
            #new_klienci.nazwa_firmy = form.nazwa_firmy
            #new_klienci.nazwisko = form.nazwisko
            #new_klienci.imie = form.imie
            #new_klienci.miasto = form.miasto
            #new_klienci.ulica = form.ulica
            #new_klienci.numer = form.numer
            #new_klienci.kod_pocztowy = form.kod_pocztowy
            #new_klienci.poczta = form.poczta
            #new_klienci.telefon = form.telefon
            new_klienci.login = request.user
            new_klienci.save()
            return HttpResponseRedirect('/sklep/') # Redirect after POST
    else:
        form = KlienciForm() # An unbound form

    return render_to_response('sklep/klienci.html',{'form': form,}, context_instance=RequestContext(request))
	

def zmien_klienta(request, id):
    klient = get_object_or_404(Klienci, login=id)
    #klient = Klienci.object.get(login=id)
    if request.method == 'POST': # If the form has been submitted...
        form = KlienciForm(request.POST or None, instance=klient) 
        forms = UserInfoForm(request.POST or None, instance=request.user)
        #forms = UserCreateForm(request.POST or None, instance=request.user)# A form bound to the POST data
        if form.is_valid() and forms.is_valid(): # All validation rules pass
            new_klienci = form.save(commit=False)
            #new_klienci.nik = form.nik
            #new_klienci.nip = form.nip
            #new_klienci.nazwa_firmy = form.nazwa_firmy
            #new_klienci.nazwisko = form.nazwisko
            #new_klienci.imie = form.imie
            #new_klienci.miasto = form.miasto
            #new_klienci.ulica = form.ulica
            #new_klienci.numer = form.numer
            #new_klienci.kod_pocztowy = form.kod_pocztowy
            #new_klienci.poczta = form.poczta
            #new_klienci.telefon = form.telefon
            new_klienci.login = request.user
            new_klienci.save()
            #new_user = form.save(commit=False)
            forms.save()
            return HttpResponseRedirect('/sklep/') # Redirect after POST
    else:
        form = KlienciForm(instance=klient)
        forms = UserInfoForm(instance=request.user)
        #forms = UserCreateForm(instance=request.user)		# An unbound form

    return render_to_response('sklep/klienci.html',{'form': form, 'forms':forms}, context_instance=RequestContext(request))

def logowanie1(request):
    koszyk = request.session.get('koszyk', [])
    kontekst = {'koszyk': []}
    
    return direct_to_template(request, 'registration/login.html', extra_context = kontekst)
	
#def logowanie(request):
#    username = request.POST['username']
#    password = request.POST['password']
#    user = authenticate(username=username, password=password)
#    if user is not None:
#        if user.is_active:
#            login(request, user)
#			return HttpResponseRedirect("sklep/base.html")
            # Redirect to a success page.
#        else:
#            return HttpResponseRedirect("/account/invalid/")
#    else:
#        return HttpResponseRedirect("/account/invalid/")

#def logout_view(request):
#    logout(request)	
#	return HttpResponseRedirect("/sklep/")
		
def strona_glowna(request):
    koszyk = request.session.get('koszyk', [])
    #if koszyk:
    #    kontekst = {'koszyk': produkty, 'formularz': formularz}
    #else:
    kontekst = {'koszyk': []}
    
    return direct_to_template(request, 'sklep/glowna.html', extra_context = kontekst)
	
def strona_kontakt(request):
    koszyk = request.session.get('koszyk', [])
    #if koszyk:
    #    kontekst = {'koszyk': produkty, 'formularz': formularz}
    #else:
    kontekst = {'koszyk': []}
    
    return direct_to_template(request, 'sklep/kontakt.html', extra_context = kontekst)

	
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
    return HttpResponseRedirect(reverse('sklep_produkty'))
	
def koszyk_usun(request, id_produktu):
    koszyk = request.session.get('koszyk', [])
    if int(id_produktu) in koszyk:
        koszyk.remove(int(id_produktu))
    request.session['koszyk'] = koszyk
    return HttpResponseRedirect(reverse('koszykobsluga'))
	
def produkty_z_kategorii(request, id_kategorii):
    kategoria1 = get_object_or_404(Kategorie, pk=int(id_kategorii))
    return object_list(
        request,
        queryset=Towary.objects.filter(kategoria=kategoria1).select_related('kategoria'),
        paginate_by=3,
        extra_context={'kategoria1': kategoria1}
    )
	
def register(request):
    if request.method == 'POST':
        formA = UserCreateForm(request.POST)
        formB = KlForm(request.POST)
        if formA.is_valid() and formB.is_valid():
            new_user = formA.save()
            new_user = authenticate(username=request.POST['username'],
            password=request.POST['password1'])
            login(request, new_user)
            new_klienci = formB.save(commit=False)
            new_klienci.nik = -1
            new_klienci.login = new_user
            new_klienci.save()
			
            return HttpResponseRedirect("/sklep/")
    else:
        formA = UserCreateForm()
        formB = KlForm()
	
    return render_to_response("registration/register.html", {
		'formA': formA,'formB': formB,}, context_instance=RequestContext(request))