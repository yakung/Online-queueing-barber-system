from django import forms
from django.core.validators import validate_email

from users.models import BarberShop, Customer


class RegisterCustomerForm(forms.Form):
    email = forms.CharField(label="อีเมล์ :", required=False, validators=[validate_email])
    email.widget.attrs['placeholder'] = 'xxx@xxx.com'

    username = forms.CharField(label='ชื่อผู้ใช้ :', required=False)
    username.widget.attrs['placeholder'] = 'username'

    pass1 = forms.CharField(label="รหัสผ่าน :", required=False, widget=forms.PasswordInput)

    pass2 = forms.CharField(label='รหัสผ่านใหม่ :', required=False, widget=forms.PasswordInput)

    name = forms.CharField(label='ชื่อลูกค้า :', required=False)

    tel = forms.CharField(label='เบอร์โทรศัพท์',required=False, max_length=10)
    tel.widget.attrs['class'] = 'form-input'

    style = forms.CharField(label='ทรงผมที่ชื่นชอบ', required=False, max_length=100)
    style.widget.attrs['placeholder'] = 'เช่น รองทรงสูง, สกีนเฮด'

    MALE = "M"
    FEMALE = "F"
    OTHER = "X"
    GENDERS = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่น'),
    )
    gender = forms.ChoiceField(label="เพศ", widget=forms.RadioSelect(), required=True, choices=GENDERS)
    gender.widget.attrs['class'] = "fontt"

    def clean_name(self):
        data = self.cleaned_data['username']
        if not data:
            raise forms.ValidationError("โปรดใส่ชื่อลูกค้า")

    def clean_username(self):
        data = self.cleaned_data['username']
        if not data:
            raise forms.ValidationError("โปรดใส่ชื่อผู้ใช้")

    def clean_style(self):
        data = self.cleaned_data['style']

        if (not data):
            raise forms.ValidationError("โปรดใส่ทรงผมที่ท่านชื่นชอบ")

        return data

    def clean_tel(self):
        data = self.cleaned_data['tel']

        if not data.isdigit():
            raise forms.ValidationError("เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
        if len(data) < 10:
            raise forms.ValidationError("เลขโทรศัพท์ต้องเท่ากับ 10 ตัว")

        return data

    def clean_pass1(self):
        data = self.cleaned_data['pass1']

        if not data:
            raise forms.ValidationError("โปรดใส่รหัสผ่าน")
        if (len(data) < 8):
            raise forms.ValidationError("รหัสผ่านต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")

        return data

    def clean_pass2(self):
        data = self.cleaned_data['pass2']

        if not data:
            raise forms.ValidationError("โปรดใส่รหัสผ่านใหม่")
        if (len(data) < 8):
            raise forms.ValidationError("รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")

        return data

    def clean(self):
        clean = super().clean()
        pass1 = clean.get('pass1')
        pass2 = clean.get('pass2')
        if (pass1 != pass2):
            raise forms.ValidationError("รหัสผ่านใหม่ กับ ยืนยันรหัสผ่านต้องเหมือนกัน")


class RegisterBarberForm(forms.Form):
    email = forms.CharField(label='อีเมล์ :', required=False, validators=[validate_email])
    email.widget.attrs['placeholder'] = 'xxx@xxx.com'

    username = forms.CharField(label='ชื่อผู้ใช้ :',required=False, )
    username.widget.attrs['placeholder'] = 'username'

    pass1 = forms.CharField(label='รหัสผ่าน :',required=False, widget=forms.PasswordInput)

    pass2 = forms.CharField(label='รหัสผ่านใหม่ :', required=False, widget=forms.PasswordInput)

    shopname = forms.CharField(label='ชื่อร้าน :',required=False, max_length=250)
    
    tel = forms.CharField(label='เบอร์โทรร้าน :',required=False, max_length=10)

    style = forms.CharField(label='ทรงผมยอดนิยม :', required=False, max_length=100)
    style.widget.attrs['placeholder'] = 'เช่น รองทรงสูง, สกีนเฮด'

    address = forms.CharField(label='สถานที่ตั้งของร้าน :',widget=forms.Textarea, required=False)

    description = forms.CharField(label='คำอธิบายร้าน :', widget=forms.Textarea, required=False)

    pic = forms.ImageField(label='รูปร้าน :', required=False)

    def clean_username(self):
        data = self.cleaned_data['username']
        if not data:
            raise forms.ValidationError("โปรดใส่ชื่อผู้ใช้")
        return data

    def clean_style(self):
        data = self.cleaned_data['style']

        if (not data):
            raise forms.ValidationError("โปรดใส่ทรงผมยอดนิยมของทางร้าน")

        return data

    def clean_address(self):
        data = self.cleaned_data['address']
        if (not data):
            raise forms.ValidationError('โปรดใส่ที่อยู่')
        return data

    def clean_desciption(self):
        data = self.cleaned_data['description']
        if (not data):
            raise forms.ValidationError('โปรดใส่รายละเอียดของร้าน')
        return data

    def clean_shopname(self):
        data = self.cleaned_data['shopname']

        if (not data):
            raise forms.ValidationError("โปรดใส่ชื่อร้าน")

        return data

    def clean_tel(self):
        data = self.cleaned_data['tel']

        if len(data) < 10:
            raise forms.ValidationError("เลขโทรศัพท์ต้องเท่ากับ 10 ตัว")
        if not data.isdigit():
            raise forms.ValidationError("เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")

        return data

    def clean_pass1(self):
        data = self.cleaned_data['pass1']
        if not data:
            raise forms.ValidationError("โปรดใส่รหัสผ่าน")
        if len(data) < 8:
            raise forms.ValidationError("รหัสผ่านต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")

        return data

    def clean_pass2(self):
        data = self.cleaned_data['pass2']

        if not data:
            raise forms.ValidationError("โปรดใส่รหัสผ่านใหม่")

        if len(data) < 8:
            raise forms.ValidationError("รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")

        return data

    def clean(self):
        clean = super().clean()
        pass1 = clean.get('pass1')
        pass2 = clean.get('pass2')
        if pass1 != pass2:
            raise forms.ValidationError("รหัสผ่านใหม่ กับ ยืนยันรหัสผ่านต้องเหมือนกัน")


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="รหัสผ่านเก่า")
    new_password1 = forms.CharField(label="รหัสผ่านใหม่")
    new_password2 = forms.CharField(label="ยืนยันรหัสผ่าน")

    def clean_newpassword1(self):
        value = self.cleaned_data['new_password1']

        if (len(value) < 8):
            raise forms.ValidationError("รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")
        return value

    def clean_newpassword2(self):
        value = self.cleaned_data['new_password2']

        if (len(value) < 8):
            raise forms.ValidationError("รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")
        return value

    def clean(self):
        clean = super().clean()
        pass1 = clean.get('new_password1')
        pass2 = clean.get('new_password2')

        if (pass1 != pass2):
            raise forms.ValidationError("รหัสผ่านใหม่ กับ ยืนยันรหัสผ่านต้องเหมือนกัน")
        elif (pass1 == pass2):
            if (len(pass1) < 8 and len(pass2) < 8):
                self.add_error('new_password1', "รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")
                self.add_error('new_password2', "รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")

class BarberShopForm(forms.ModelForm):
    class Meta:
        model = BarberShop
        fields = ['shopname', 'tel', 'address', 'style', 'description', 'pic']
        labels = {
            "shopname": "ชื่อร้าน",
            'tel':'เบอร์โทรร้าน',
            'address':'ที่อยู่ของร้าน',
            'style':'ทรงผมยอดนิยม',
            'description':'คำอธิบายร้าน',
            'pic':'รูปร้าน'
        }

class CustomerForm(forms.ModelForm):
    style = forms.CharField(max_length=100,required=False)
    class Meta:
        model = Customer
        fields = ['name', 'tel', 'style', 'gender']
        labels = {
            "name": "ชื่อลูกค้า",
            'tel': 'เบอร์โทร',
            'style': 'ทรงผมที่ชื่นชอบ',
            'gender': 'เพศ'
        }

class LoginForm(forms.Form):
    username = forms.CharField(label='username', required=False, )
    password = forms.CharField(label="password", required=False, widget=forms.PasswordInput)
