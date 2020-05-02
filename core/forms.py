from django import forms
from django_countries.fields import CountryField
PAYMENT_CHOICES = (
    ('S','Stripe'),
    ('P','Paypal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    country = CountryField(blank_label='(Select country)').formfield(attrs={
        'class':'custom-select d-block w-100'
    })
    zip  = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES,required=False)


class CoponForm(forms.Form):
    code = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'PromoCode'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'4'}))
    email = forms.EmailField()


