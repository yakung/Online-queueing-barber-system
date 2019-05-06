from django import forms

from core.models import Review


class BlogForm(forms.Form):
    header = forms.CharField(label='หัวข้อ' ,max_length=255, required=False)
    content = forms.CharField(label='บทความ',widget=forms.Textarea, required=False)
    picture = forms.ImageField(label='รูปภาพ',required=False)

    def clean_header(self):
        data = self.cleaned_data['header']
        if not data:
            raise forms.ValidationError('โปรดเขียนหัวข้อ')

        return data

    def clean_content(self):
        data = self.cleaned_data['content']
        if not data:
            raise forms.ValidationError('โปรดเขียนรายละเอียด')
        return data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['customer', 'barbershop', 'date', 'rating']
        labels={
            'description':'คำอธิบายเกี่ยวกับร้าน',
        }