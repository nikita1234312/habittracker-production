from django import forms
from profiles import models


class ProfileEditForm(forms.ModelForm):
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш город'}))

    class Meta:
        model = models.ProfileModel
        fields = ['city', 'avatar', 'cover_image']


