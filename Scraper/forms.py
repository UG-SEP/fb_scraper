from django import forms

class FacebookPostForm(forms.Form):
    url = forms.URLField(label="Facebook Post URL", required=True)
