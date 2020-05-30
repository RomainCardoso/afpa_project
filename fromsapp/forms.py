from django import forms

class ContactForm(forms.Form):
    item = forms.CharField()


class HiddenForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput(), initial='{{ name }}')
    amazon_price = forms.CharField(widget=forms.HiddenInput(), initial='{{ amazon_price }}')
    ldlc_price = forms.CharField(widget=forms.HiddenInput(), initial='{{ ldlc_price }}')
    maxgaming_price = forms.CharField(widget=forms.HiddenInput(), initial='{{ maxgaming_price }}')
    amazon_url = forms.CharField(widget=forms.HiddenInput(), initial='{{ amazon_url }}')
    ldlc_url = forms.CharField(widget=forms.HiddenInput(), initial='{{ ldlc_url }}')
    maxgaming_url = forms.CharField(widget=forms.HiddenInput(), initial='{{ maxgaming_url }}')
