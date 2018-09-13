from django import forms

from accounts.models import Avatar


class AvatarEditForm(forms.Form):
    temp_image = forms.ImageField(label='Image file',
                                  required=False)

    x1 = forms.IntegerField(required=False)
    y1 = forms.IntegerField(required=False)
    x2 = forms.IntegerField(required=False)
    y2 = forms.IntegerField(required=False)
