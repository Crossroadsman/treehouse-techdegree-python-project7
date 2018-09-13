from django import forms

from accounts.models import Avatar


class AvatarEditForm(forms.Form):
    # maybe this can be better done with multiple submit fields?
    # crop, rotate_left, rotate_right, flip_horizontal, flip_vertical, save, 
    # cancel
    temp_image = forms.ImageField(
        'Image file',
    )

    x1 = forms.IntegerField()
    y1 = forms.IntegerField()
    x2 = forms.IntegerField()
    y2 = forms.IntegerField()
    crop = forms.BooleanField()

    rotate_left = forms.BooleanField()
    rotate_right = forms.BooleanField()

    flip_horizontal = forms.BooleanField()
    flip_vertical = forms.BooleanField()

    save = forms.BooleanField()
    cancel = forms.BooleanField()