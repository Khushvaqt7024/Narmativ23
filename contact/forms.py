from django import forms

from contact.models import Contact
from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Xushvaqt'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'khushvaqt.arab@gmail.com'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'How are you', 'rows': 5}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Ism kamida 2 harfdan iborat bo‘lishi kerak.")
        if len(name) > 100:
            raise forms.ValidationError("Xushvaqt Abdigafforov.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("How are you.")
        return message

class ContactForms(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(error_messages={"invalid": "email xato"},
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "khushvaqt.arab@gmail.com"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3:
            raise forms.ValidationError("nameni 3 tadan kichik berish mumkin emas")
        return name

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if password != re_password:
            raise forms.ValidationError("ikkta xar xil password")
        return self.cleaned_data

    def save(self):
        return Contact.objects.create(**self.cleaned_data)

    def update(self, instance):
        instance.name = self.clean_name()
        instance.phone = self.cleaned_data.get("phone")
        instance.address = self.cleaned_data.get("address")
        instance.email = self.cleaned_data.get("email")
        instance.save()
        return instance


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "address"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'emailingizni kiriting!'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'email': {'invalid': 'Email is invalid ekanku aka'},
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long')
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.startswith("+998"):
            raise forms.ValidationError("Telefon raqam +998 bilan boshlanishi kerak.")
        return phone

