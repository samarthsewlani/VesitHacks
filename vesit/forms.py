
from django import forms
from . import models as vesit_models
from tempus_dominus.widgets import DateTimePicker



class DateForm(forms.Form):
    
    start_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': False,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    end_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': False,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )


class EventCreateForm(forms.ModelForm):

    class Meta:
        model = vesit_models.Event
        fields = [ 'name', 'description' , 'event_type', 'location' ]

