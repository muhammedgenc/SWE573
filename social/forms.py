from django import forms
from .models import Service, ServiceApplication, Event, EventApplication
from django.forms.widgets import DateInput, TimeInput

choices = [('General','General'),
           ('Technology','Technology'),
           ('Art','Art'),
           ('Culinary','Culinary'),
           ('Finance','Finance'),
           ('Business','Business'),
           ('Games','Games'),
           ('Sports', 'Sports')]

class ServiceForm(forms.ModelForm):

	class Meta:
		model = Service
		fields = ['name', 'description', 'service_date', 'service_time', 'duration', 'location', 'capacity', 'picture', 'category']
		widgets = {
            'name':forms.Textarea(attrs={'rows': '1','class': 'form-control','placeholder': 'Service Name'}),
            'description':forms.Textarea(attrs={'rows': '5','class': 'form-control','placeholder': 'Service Description'}), 
            'category':forms.Select(choices= choices, attrs={'class': 'form-control'}),
            'service_date': DateInput(attrs={'type': 'date'}),
            'service_time': TimeInput(format=('%H:%M'),attrs={'type': 'time'}),
            'duration': forms.NumberInput(),
            'capacity': forms.NumberInput(),
            'location': forms.Textarea(attrs={'rows': '1','class': 'form-control','placeholder': 'Location of the Service'}),
        }

class ServiceApplicationForm(forms.ModelForm):    

    class Meta: 
        model = ServiceApplication
        fields = []

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date', 'event_time', 'duration', 'location', 'capacity', 'picture', 'category']
        widgets = { 
            'name':forms.Textarea(attrs={'rows': '1','class': 'form-control','placeholder': 'Event Name'}),
            'description':forms.Textarea(attrs={'rows': '5','class': 'form-control','placeholder': 'Event Description'}), 
            'category':forms.Select(choices= choices, attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(format=('%H:%M'),attrs={'type': 'time'}),
            'duration': forms.NumberInput(),
            'capacity': forms.NumberInput(),
            'location': forms.Textarea(attrs={'rows': '1','class': 'form-control','placeholder': 'Location of the Event'}),
       }
        
class EventApplicationForm(forms.ModelForm):    

    class Meta: 
        model = EventApplication
        fields = []
