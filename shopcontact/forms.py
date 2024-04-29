from django import forms
from django.core.validators import MaxLengthValidator


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی', 'class': 'form-control'}),
        label='نام و نام خانوادگی'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل', 'class': 'form-control'}),
        label='ایمیل'
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'موضوع', 'class': 'form-control'}),
        label='موضوع'
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'متن پیام', 'class': 'form-control'}),
        label='پیام',
        validators=[MaxLengthValidator(1000, 'متن پیام نمی تواند بیشتر از 1000 کاراکتر باشد')]
    )
