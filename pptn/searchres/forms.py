from django import forms

class cuisineForm(forms.Form):
    food_type = forms.CharField(label='Food Type', max_length=100, widget=forms.TextInput(attrs={'placeholder':'burgers, pizza...'}))
    city = forms.CharField(label='City', max_length=100)
    address = forms.CharField(label='Address', max_length=100)
