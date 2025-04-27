from django import forms
from .models import Profile
from django.utils.translation import gettext_lazy as _

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'phone']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'image': _('Profile Image'),
            'bio': _('Bio'),
            'phone': _('Phone Number'),
        }