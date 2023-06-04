from rest_framework import serializers
from .models import Profile, User, Question, Preference, ProfileImage, Tag, Location, OTPVerify


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "icon")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = "__all__"

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"    

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"    

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.CharField(source="User.email")
    class Meta:
        model = OTPVerify
        fields = ("email_otp", "email")