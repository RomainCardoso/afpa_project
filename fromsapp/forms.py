from django import forms

class ContactForm(forms.Form):
    item = forms.CharField()
