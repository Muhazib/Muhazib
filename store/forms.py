from django import forms
from store.models.address import Address
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['pincode', 'area', 'locality', 'town', 'village', 'name', 'phone', 'alt_phone']
