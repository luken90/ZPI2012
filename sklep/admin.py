from django.contrib import admin
from sklep.models import *

class TowaryAdmin(admin.ModelAdmin):
   list_display = ('nazwa_towaru', 'cena_sklepowa')
   #date_hierarchy = 'dostepne_od'
   search_fields = ('nazwa_towaru',)
   
class KlientAdmin(admin.ModelAdmin):
	list_display = ('nazwisko', 'imie', 'login')
	search_fields = ('nazwisko', 'login',)
	
class DostawcyAdmin(admin.ModelAdmin):
	list_display = ('nazwa_dostawcy', 'telefon')
	search_fields = ('nazwa_dostawcy', 'regon',)

class PracownicyAdmin(admin.ModelAdmin):
	list_display = ('nazwisko', 'imie', 'pesel')
	search_fields = ('nazwisko', 'login',)	
	
admin.site.register(Klienci, KlientAdmin)
admin.site.register(Stanowiska)
admin.site.register(Dostawcy, DostawcyAdmin)
admin.site.register(Pracownicy, PracownicyAdmin)
admin.site.register(Hasla)
#admin.site.register(Towary)
admin.site.register(Towary, TowaryAdmin)
admin.site.register(Dostawy)
admin.site.register(OpisyDostaw)
admin.site.register(Zamowienia)
admin.site.register(OpisyZamowien)
admin.site.register(Ksiegowosc)
admin.site.register(Kategorie)