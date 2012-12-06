
# -*- coding: utf-8 -*-

import re
from django import forms

from django.contrib.localflavor.pl.forms import PLPostalCodeField
from sklep.models import Towary, Klienci, Stanowiska, Zamowienia, OpisyZamowien
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
 
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
 
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
		
class UserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('email',)


class ZamowienieForm(forms.Form):

    email = forms.EmailField()

    imie_nazwisko = forms.CharField(label=u'Imie i nazwisko', max_length=60)

    adres = forms.CharField(max_length=100)

    kod_pocztowy = PLPostalCodeField()

    miasto = forms.CharField(max_length=60)

    uwagi = forms.CharField(widget=forms.Textarea, required=False)
	
class TowarForm(forms.Form):
    
	idtowaru = forms.CharField(max_length=255, required=True)
	nazwa_towaru = forms.CharField(max_length=255, required=True)
	ilosc_w_sklepie = forms.CharField(max_length=10, required=True)
	cena_sklepowa = forms.CharField(max_length=10, required=True)
	minimum_towar = forms.CharField(max_length=10, required=True)
	opis = forms.CharField(max_length=1000)
	zdjecie = forms.CharField(max_length=1000)
	kategoria = forms.CharField(max_length=10, required=True)
	
#class KlienciForm(forms.Form):
    
#	nik = forms.CharField(max_length=255, required=True)
#	nip = forms.CharField(max_length=255, required=True)
#	nazwa_firmy = forms.CharField(max_length=255, required=True)
#	nazwisko= forms.CharField(max_length=255, required=True)
#	imie = forms.CharField(max_length=255, required=True)
#	miasto = forms.CharField(max_length=255, required=True)
#	ulica = forms.CharField(max_length=1000)
#	numer = forms.CharField(max_length=1000)
#	kod_pocztowy = forms.CharField(max_length=255, required=True)
#	poczta = forms.CharField(max_length=255, required=True)
#	telefon = forms.CharField(max_length=255, required=True)
#	login = forms.CharField(max_length=255, required=True)
	
#class KlienciForm(forms.ModelForm):
#	class Meta:
#		model = Klienci
    
    		
#    def save(self, commit=True):
#        user = super(KlienciForm, self).save(commit=False)
#        user.nip = self.cleaned_data['nip']
#        if user.nip == '':
#            user.nip = None
#        return user
		
class KlienciForm(forms.ModelForm):
    class Meta:
        model = Klienci

    def clean_nip(self):
        nip = self.cleaned_data.get('nip')
        if not nip:
            nip = None
        return nip

		
class KlForm(forms.ModelForm):
    kod_pocztowy = forms.RegexField(regex =r'^\d{2}-\d{3}$',error_message = ("Podaj kod w postaci XX-XXX"))
    nip = forms.RegexField(regex =r'^\d{10}$|^\d{11}$|\s$',error_message = ("Podaj kod z 10 lub 11 cyfr"))
    #imie = forms.RegexField(regex =r'^[A-Zia-z?]{1}([a-z????]+|\s[A-Zi][a-z????]*){1,30}$',error_message = ("Tylko litery"))
    #nazwisko = forms.RegexField(regex =r'^[A-Z?????-z????]{1}([a-z????]+|\s*-*[A-Z?????[a-z????]){1,30}$',error_message = ("Tylko litery"))
    #miasto = forms.RegexField(regex =r'^[¶¿¼¦¯¬]{1,30}$',error_message = ("Tylko litery"))
    #miasto = forms.RegexField(regex =r'(?iL)^[\s\*\?a-z]*$',error_message = ("Tylko litery polskie"))
    #miasto = forms.RegexField(re.compile(r'^\w+', flags=re.UNICODE|re.IGNORE))
    #miasto = forms.RegexField(regex =r'^(?L)/$'',error_message = ("Tylko litery")
    #telefon = forms.RegexField(regex =r'^\d{7,9}|\d{0}$',error_message = ("Podaj tylko cyfry. Od 7 do 9"))
	
    class Meta:
        model = Klienci
		
    def clean_nip(self):
        nip = self.cleaned_data.get('nip')
        if not nip or nip == " ":
            nip = None
        return nip
		
    def clean_nazwisko(self):
        if self.cleaned_data['nazwisko'].isalpha():
            return self.cleaned_data['nazwisko']
        else:
            raise ValidationError("Tylko litery")		

    def clean_imie(self):
        if self.cleaned_data['imie'].isalpha():
            return self.cleaned_data['imie']
        else:
            raise ValidationError("Tylko litery")			
			
    def clean_poczta(self):
        if self.cleaned_data['poczta'].isalpha():
            return self.cleaned_data['poczta']
        else:
            raise ValidationError("Tylko litery")				
			
    def clean_miasto(self):
        if self.cleaned_data['miasto'].isalpha():
            return self.cleaned_data['miasto']
        else:
            raise ValidationError("Tylko litery")
		
 #   def clean_nazwa_firmy(self):
 #       nazwa_firmy = self.cleaned_data.get('nazwa_firmy')
 #       if not nazwa_firmy or nazwa_firmy == " ":
 #           nazwa_firmy = None
 #       return nazwa_firmy
		
 #   def clean_imie(self):
 #       imie = self.cleaned_data.get('imie')
 #       if not imie or imie == " ":
 #           imie = None
 #       return imie
		
 #   def clean_nazwisko(self):
 #       nazwisko = self.cleaned_data.get('nazwisko')
 #       if not nazwisko or nazwisko == " ":
 #           nazwisko = None
 #       return nazwisko


		
class StanowiskaForm(forms.ModelForm):
    class Meta:
        model = Stanowiska	

class ZamowieniaForm(forms.ModelForm):
    class Meta:
	    model = Zamowienia
		
class OpisyZamowienForm(forms.ModelForm):
    class Meta:
	    model = OpisyZamowien
		
    #def clean_ilosc(self):
    #    if self.cleaned_data['ilosc']>0:
    #        return self.cleaned_data['ilosc']
    #    else:
    #        raise ValidationError("IloÅ›Ä‡ musi byÄ‡ dodatnia")	