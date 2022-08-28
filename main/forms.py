from django import forms
from .models import *
from django.forms import ModelForm

class CalorieCal(forms.Form):

   CASES = [
      ('1','Sedentry'),
      ('2','Moderate'),
      ('3','Extreme')
   ]
   gender = [
      ('Male','Male'),
      ('Female','Female')
   ]
   
   Age=forms.IntegerField(label='AGE:',widget=forms.TextInput(attrs={'placeholder': 'Age'}))
   Weight=forms.IntegerField(label='Weight:',widget=forms.TextInput(attrs={'placeholder': 'Weight'}))
   WeightChoice=forms.CharField(widget=forms.RadioSelect(choices=[('LB','LB'),('KG','KG')]))
   #Height for US
   Height=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Height in CM','class':'US'}),required=False)
   #Height for metric
   #Feet
   Height_1st=forms.IntegerField(label='Height (Feet)',widget=forms.TextInput(attrs={'placeholder': 'Height in Feet','class':'metric',}),required=False)
   Height_2nd=forms.IntegerField(label='Height (Inches)',widget=forms.TextInput(attrs={'placeholder': 'Height in inches','class':'metric'}),required=False)
   HeightChoice=forms.CharField(widget=forms.RadioSelect(choices=[('CM','CM'),('Feet','Feet')],attrs={'class':'heightChoice CM','onchange':'myFunction(this.value)'}))
   
   Gender=forms.CharField(widget=forms.RadioSelect(choices=gender))
   CalType=forms.CharField(widget=forms.Select(choices=[('Losing Weight','Losing Weight'),('Gaining Muscle','Gaining Muscle')]))
   Activity=forms.CharField(max_length=50,widget=forms.Select(choices=CASES))


