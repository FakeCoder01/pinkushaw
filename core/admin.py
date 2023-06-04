from django.contrib import admin
from .models import Profile, ProfileImage, Preference, Location, Question, LeftSwipe, RightSwipe, OTPVerify, Match, Tag
# Register your models here.

admin.site.register(Profile)
admin.site.register(ProfileImage)
admin.site.register(Preference)
admin.site.register(Location)
admin.site.register(Question)
admin.site.register(LeftSwipe)
admin.site.register(RightSwipe)
admin.site.register(OTPVerify)
admin.site.register(Match)
admin.site.register(Tag)