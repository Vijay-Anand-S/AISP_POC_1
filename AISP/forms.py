from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Text', max_length=300)