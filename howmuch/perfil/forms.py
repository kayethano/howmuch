from django import forms
from django.forms import ModelForm, Textarea, TextInput
from howmuch.perfil.models import Perfil

class PerfilForm(ModelForm):
	class Meta:
		model = Perfil
		exclude = ('user', )
		widgets = {
			'company' : TextInput(attrs={'class':'InputFormRequestItem',}),
			'address' : Textarea(attrs={'class':'InputFormRequestItem', 'cols': 40, 'rows': 5}),
            'address2': Textarea(attrs={'class':'InputFormRequestItem','cols': 40, 'rows': 5}),
            'city' : TextInput(attrs={'class':'InputFormRequestItem',}),
            'zipcode' : TextInput(attrs={'class':'InputFormRequestItem',}),
            'state' : TextInput(attrs={'class':'InputFormRequestItem',}),
        	'phone' : TextInput(attrs={'class':'InputFormRequestItem',}),
            'bank' : TextInput(attrs={'class':'InputFormRequestItem',}),
            'account_bank' : TextInput(attrs={'class':'InputFormRequestItem',}),
            'account_paypal' : TextInput(attrs={'class':'InputFormRequestItem',}),
        }