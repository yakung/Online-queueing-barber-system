from django import forms

class BlogForm(forms.Form):
    header = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea, required=False)
    picture = forms.ImageField(required=False)

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