from django import forms

from .models import Queue


class DateInput(forms.DateInput):
    input_type = 'date'


class QueueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(QueueForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['hairstyle'].required = False
        self.fields['ref_pic'].required = False

    class Meta:
        model = Queue
        fields = ['start_queue', 'end_queue', 'ref_pic', 'hairstyle']
        widgets = {
            'start_queue': DateInput(),
            'end_queue': DateInput()
        }

    def clean_start_queue(self):
        data = self.cleaned_data.get('start_queue')

        if (not data):
            raise forms.ValidationError('โปรดใส่เวลาจองคิว')
        return data

    def clean_end_queue(self):
        data = self.cleaned_data.get('end_queue')

        if (not data):
            raise forms.ValidationError('โปรดใส่เวลาจองคิว')

        return data
