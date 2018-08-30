from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
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

