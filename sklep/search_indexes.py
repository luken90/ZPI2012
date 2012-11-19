import datetime
from haystack.indexes import *
from sklep.models import Towary
from haystack import site


class TowaryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    nazwa_towaru = CharField(model_attr='nazwa_towaru')
	
	
    def get_model(self):
        return Towary
		

    def index_queryset(self):
        #"""Used when the entire index for model is updated."""
        return self.get_model().objects.all()
		

site.register(Towary, TowaryIndex)		
		
		
		

