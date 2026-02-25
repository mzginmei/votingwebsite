from django.contrib.auth.forms import UserCreationForm

from .models import Voter


class VoterRegistrationForm(UserCreationForm):
    class Meta:
        model = Voter
        fields = ("email", "full_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
