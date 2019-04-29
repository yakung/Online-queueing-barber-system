from django import forms

from .models import Queue


class QueueForm(forms.Form):
    start_queue = forms.DateTimeField()
    end_queue = forms.DateTimeField()
    hairstyle = forms.CharField(max_length=100, required=False)
    ref_pic = forms.ImageField(required=False)

    # class Meta:
    #     model = Queue
    #     fields = ['start_queue', 'end_queue', 'ref_pic', 'hairstyle']

    def clean_start_queue(self):
        data = self.cleaned_data.get('start_queue')

        if (not data):
            raise forms.ValidationError('โปรดใส่เวลาจองคิว')

    def clean_end_queue(self):
        data = self.cleaned_data.get('end_queue')

        if (not data):
            raise forms.ValidationError('โปรดใส่เวลาจองคิว')
