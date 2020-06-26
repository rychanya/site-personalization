from django import forms

class NumberForm(forms.Form):
    number = forms.IntegerField(max_value=100, min_value=0)
