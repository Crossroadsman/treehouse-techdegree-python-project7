from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):

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
                  "bio",
                  "given_name",
                  "family_name",
                  "avatar",
                  "city",
                  "state",
                  "country",
                  "favourite_animal",
                  "hobby",
                  "favourite_fountain_pen",
                  )
        

