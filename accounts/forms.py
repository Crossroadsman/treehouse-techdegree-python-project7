from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    # It is valid to explicitly instantiate a form field that has a 
    # corresponding model field, but such a field will not take any of the
    # defaults from the model
    date_of_birth = forms.DateField(
        label="Date of birth",
        input_formats = ['%Y-%m-%d',      # '2006-10-25'
                         '%m/%d/%Y',      # '10/25/2006'
                         '%d/%m/%y']      # '25/10/06'
    )
    # bio = forms.CharField(widget=CKEditorWidget())

    # Note that method declarations for cleaning must come before the
    # Meta class declaration.
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) < 10:
            raise forms.ValidationError("Bio must be at least 10 characters")
        return bio

    class Meta:
        model = UserProfile
        fields = ("date_of_birth",
                  "given_name",
                  "family_name",
                  "bio",
                  "city",
                  "state",
                  "country",
                  "favourite_animal",
                  "hobby",
                  "favourite_fountain_pen",
                  )
        labels = {
            "given_name": "First name",
            "family_name": "Last name",
        }
        

