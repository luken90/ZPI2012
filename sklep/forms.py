# coding: utf-8

from django import forms

from django.contrib.localflavor.pl.forms import PLPostalCodeField

from sklep.models import Towary, Klienci, Stanowiska, Zamowienia, OpisyZamowien


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
	
class KlienciForm(forms.ModelForm):
	class Meta:
		model = Klienci

class StanowiskaForm(forms.ModelForm):
    class Meta:
        model = Stanowiska	

class ZamowieniaForm(forms.ModelForm):
    class Meta:
	    model = Zamowienia
		
class OpisyZamowienForm(forms.ModelForm):
    class Meta:
	    model = OpisyZamowien