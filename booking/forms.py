from datetime import datetime

from django import forms

from .models import Queue

#
# class DateInput(forms.DateInput):
#     input_type = 'date'
#
#
# class QueueForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         # first call parent's constructor
#         super(QueueForm, self).__init__(*args, **kwargs)
#         # there's a `fields` property now
#         self.fields['hairstyle'].required = False
#         self.fields['ref_pic'].required = False
#
#     class Meta:
#         model = Queue
#         fields = ['start_queue', 'end_queue', 'ref_pic', 'hairstyle']
#         widgets = {
#             'start_queue': DateInput(),
#             'end_queue': DateInput()
#         }
#
#
#     def clean(self):
#         clean = super().clean()
#         day1 = clean.get('start_queue')
#         day2 = clean.get('end_queue')
#         # if day2 < day1:
#         #     self.add_error('end_queue', 'วันที่ไม่ถูกต้อง')