# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm

class Klienci(models.Model):
    nik = models.BigIntegerField(primary_key=True)
    nip = models.CharField(max_length=15, unique=True, blank=True)
    nazwa_firmy = models.CharField(max_length=50, blank=True)
    nazwisko = models.CharField(max_length=30, blank=True)
    imie = models.CharField(max_length=30, blank=True)
    miasto = models.CharField(max_length=30)
    ulica = models.CharField(max_length=40, blank=True)
    numer = models.CharField(max_length=7)
    kod_pocztowy = models.CharField(max_length=6)
    poczta = models.CharField(max_length=30)
    telefon = models.CharField(max_length=13, blank=True)
    login = models.CharField(max_length=20, blank=True)
    class Meta:
		verbose_name='Klient'
		db_table = u'klienci'
		verbose_name_plural = 'Klienci'
		ordering = ('nik',)

    def __unicode__(self):
        return self.nazwisko

class Stanowiska(models.Model):
    identyfikator = models.BigIntegerField(primary_key=True)
    stanowisko = models.CharField(max_length=50, unique=True)
    class Meta:
		verbose_name='Stanowisko'
		db_table = u'stanowiska'
		verbose_name_plural = 'Stanowiska'
		ordering = ('identyfikator',)

    def __unicode__(self):
        return self.stanowisko

class Dostawcy(models.Model):
    nid = models.BigIntegerField(primary_key=True)
    regon = models.BigIntegerField(unique=True)
    nip = models.CharField(max_length=15, unique=True)
    nazwa_dostawcy = models.CharField(max_length=30)
    miasto = models.CharField(max_length=30)
    ulica = models.CharField(max_length=40, blank=True)
    numer = models.CharField(max_length=7)
    kod_pocztowy = models.CharField(max_length=6)
    poczta = models.CharField(max_length=30)
    telefon = models.CharField(max_length=13, blank=True)
    class Meta:
		verbose_name='Dostawca'
		db_table = u'dostawcy'
		verbose_name_plural = 'Dostawcy'
		ordering = ('nid',)

    def __unicode__(self):
        return self.nazwa_dostawcy

class Pracownicy(models.Model):
    np = models.BigIntegerField(primary_key=True)
    nazwisko = models.CharField(max_length=30)
    imie = models.CharField(max_length=30)
    pesel = models.CharField(max_length=15, unique=True)
    nip = models.CharField(max_length=15, unique=True)
    miasto = models.CharField(max_length=30)
    ulica = models.CharField(max_length=40, blank=True)
    numer = models.CharField(max_length=7)
    kod_pocztowy = models.CharField(max_length=6)
    poczta = models.CharField(max_length=30)
    stanowisko = models.ForeignKey(Stanowiska, db_column='stanowisko')
    class Meta:
		verbose_name='Pracownik'
		db_table = u'pracownicy'
		verbose_name_plural = 'Pracownicy'
		ordering = ('np',)

    def __unicode__(self):
        return self.nazwisko

class Hasla(models.Model):
    identyfikator = models.ForeignKey(Pracownicy, unique=True, db_column='identyfikator')
    login = models.CharField(max_length=50, unique=True)
    haslo = models.CharField(max_length=20)
    class Meta:
		verbose_name='Haslo'
		db_table = u'hasla'
		verbose_name_plural = 'Hasla'
		ordering = ('identyfikator',)

    def __unicode__(self):
        return self.login

class Kategorie(models.Model):
    identyfikator = models.BigIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=30, unique=True)
    class Meta:
		verbose_name='Kategoria'
		db_table = u'kategorie'
		verbose_name_plural = 'Kategorie'
		ordering = ('identyfikator',)

    def __unicode__(self):
        return self.nazwa	
	
	#@permalink
	#def get_absolute_url(self):
	#	return ('sklep_kategoria', (self.pk,)) 
	
    def get_absolute_url(self):
        return reverse('sklep_kategoria', args=[self.pk,])

class Towary(models.Model):
    idtowaru = models.BigIntegerField(primary_key=True)
    nazwa_towaru = models.CharField(max_length=255, unique=True)
    ilosc_w_sklepie = models.BigIntegerField()
    cena_sklepowa = models.BigIntegerField()
    minimum_towar = models.BigIntegerField()
    opis = models.CharField(max_length=1000, blank=True)
    zdjecie = models.CharField(max_length=255, blank=True)
    kategoria = models.ForeignKey(Kategorie, db_column='kategoria')
    class Meta:
		verbose_name='Towar'
		db_table = u'towary'
		verbose_name_plural = 'Towary'
		ordering = ('idtowaru',)

    def __unicode__(self):
        return self.nazwa_towaru

class Dostawy(models.Model):
    iddostawy = models.BigIntegerField(primary_key=True)
    nid = models.ForeignKey(Dostawcy, db_column='nid')
    data_dostawy = models.DateField()
    status = models.CharField(max_length=20)
    np = models.ForeignKey(Pracownicy, db_column='np')
    class Meta:
		verbose_name='Dostawa'
		db_table = u'dostawy'
		verbose_name_plural = 'Dostawy'
		ordering = ('iddostawy',)

class OpisyDostaw(models.Model):
    iddostawy = models.ForeignKey(Dostawy, unique=True, db_column='iddostawy')
    idtowaru = models.ForeignKey(Towary, unique=True, db_column='idtowaru')
    ilosc = models.BigIntegerField()
    cena_producenta = models.BigIntegerField()
    class Meta:
		verbose_name='Opis dostawy'
		db_table = u'opisy_dostaw'
		verbose_name_plural = 'Opisy dostaw'
		ordering = ('iddostawy','idtowaru',)

class Zamowienia(models.Model):
    idzamowienia = models.BigIntegerField(primary_key=True)
    nik = models.ForeignKey(Klienci, db_column='nik')
    np = models.ForeignKey(Pracownicy, db_column='np')
    data_zamowienia = models.DateField()
    status = models.CharField(max_length=20)
    class Meta:
		verbose_name='Zamowienie'
		db_table = u'zamowienia'
		verbose_name_plural = 'Zamowienia'
		ordering = ('idzamowienia',)

class OpisyZamowien(models.Model):
    idzamowienia = models.ForeignKey(Zamowienia, unique=True, db_column='idzamowienia')
    idtowaru = models.ForeignKey(Towary, unique=True, db_column='idtowaru')
    ilosc = models.BigIntegerField()
    class Meta:
		verbose_name='Opis zamowienia'
		db_table = u'opisy_zamowien'
		verbose_name_plural = 'Opisy zamowien'
		ordering = ('idzamowienia','idtowaru',)


class Ksiegowosc(models.Model):
    idtransakcji = models.BigIntegerField(primary_key=True)
    data_wykonania = models.DateField()
    kwota = models.BigIntegerField()
    np = models.ForeignKey(Pracownicy, db_column='np')
    idzamowienia = models.ForeignKey(Zamowienia, null=True, db_column='idzamowienia', blank=True)
    iddostawy = models.ForeignKey(Dostawy, null=True, db_column='iddostawy', blank=True)
    class Meta:
		verbose_name='Ksiegowosc'
		db_table = u'ksiegowosc'
		verbose_name_plural = 'Ksiegowosc'
		ordering = ('idtransakcji',)

