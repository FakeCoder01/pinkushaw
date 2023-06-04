from django import forms
from .models import Profile, ProfileImage

class ImageUploadForm(forms.ModelForm):
    model = ProfileImage
    fields = ("caption", "image")

class ProfilePicUploadForm(forms.ModelForm):
    model = Profile
    fields = ("profile_pic")
