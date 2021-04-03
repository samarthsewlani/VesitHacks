from django.shortcuts import render
from .models import Event
from django import forms
# Create your views here.

def home(request):
    return render( request, 'vesit/home.html' )


class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','description','start_time','end_time','event_type']

def index(request):
    event_form=EventForm()
    return render(request, 'vesit/index.html',{'event_form':event_form})