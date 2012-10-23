# coding: utf-8

from django import forms

from django.contrib.localflavor.pl.forms import PLPostalCodeField



class ZamowienieForm(forms.Form):

    email = forms.EmailField()

    imie_nazwisko = forms.CharField(label=u'Imie i nazwisko', max_length=60)

    adres = forms.CharField(max_length=100)

    kod_pocztowy = PLPostalCodeField()

    miasto = forms.CharField(max_length=60)

    uwagi = forms.CharField(widget=forms.Textarea, required=False)