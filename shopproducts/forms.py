from django import forms


class CommentForm(forms.Form):
    user = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='نام کاربری'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='ایمیل'
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='متن نظر'
    )
