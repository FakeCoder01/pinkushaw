from rest_framework import serializers
from core.models import Match, LeftSwipe, RightSwipe, Profile, Tag

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"

class LeftSwipeSerializer(serializers.ModelSerializer):
    profile_id = serializers.CharField(source="Profile.id")
    class Meta:
        model = LeftSwipe
        fields = ("profile_id",)     


class RightSwipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightSwipe
        fields = ("whom_liked", )  

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "icon")

class RecommendProfileSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="location.city")
    tag_names = TagSerializer(source='tags', read_only=True, many=True)
    class Meta:
        model = Profile        
        fields = ("id", "name", "profile_pic", "age", "gender", "bio", "city", "tag_names")