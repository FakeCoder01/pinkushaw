from core.models import Profile, Location, Preference, Question, LeftSwipe, RightSwipe
from django.db.models import Q 
from .serializers import RecommendProfileSerializer

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response

import math
from collections import defaultdict

# constants
SIMILARITY_THRESHOLD = 4
MAX_RECOMMENDATIONS = 32
MAX_DISTANCE = 50

def calculate_distance(lat1, lng1, lat2, lng2):
    # calculate the distance between two sets of latitude and longitude coordinates
    # using the Haversine formula to calculate distance   
    R = 6371  # radius of the earth in km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *  math.sin(dlng / 2) * math.sin(dlng / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


class RecommendProfiles(viewsets.ModelViewSet):
    serializer_class = RecommendProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return self.request.user.userprofile
    
    def get_recommendations(self, request):
        user_profile = self.request.user.userprofile
        user_preference = user_profile.preference       # retrieve user preferences
        user_location = user_profile.location           # retrieve user location
        user_tags = user_profile.tags.all()             # retrieve user tags
        user_questions = user_profile.question          # retrieve user question

        # Retrieve user left-swiped profiles
        left_swipes = LeftSwipe.objects.get(user=user_profile).disliked_users.all() # if LeftSwipe.objects.filter(
          #  user=user_profile).exists() else []

        # Retrieve user right-swiped profiles
        right_swipes = RightSwipe.objects.filter(whom_liked=user_profile)


        lat_min = user_location.lat - (MAX_DISTANCE / 111.0)
        lat_max = user_location.lat + (MAX_DISTANCE / 111.0)
        lng_min = user_location.lng - (MAX_DISTANCE / (111.0 * math.cos(math.radians(user_location.lat))))
        lng_max = user_location.lng + (MAX_DISTANCE / (111.0 * math.cos(math.radians(user_location.lat))))

        # Filter profiles based on proximity
        nearby_profiles = Profile.objects.filter(
            location__lat__range=(lat_min, lat_max),
            location__lng__range=(lng_min, lng_max)
        ).exclude(user=self.request.user).exclude(id__in=left_swipes)

        # calculate similarity scores
        potential_matches = defaultdict(int)
        for profile in nearby_profiles:
            similarity_score = 0

            # compare gender preference (strict)
            if user_preference.gender_preference == profile.gender and user_profile.gender == profile.preference.gender_preference:
                similarity_score += 1
            else:
                continue    
            # compare age preferences (strict)
            if (user_preference.min_age_preference <= profile.age <= user_preference.max_age_preference) or (
                    profile.preference.min_age_preference <= user_profile.age <= profile.preference.max_age_preference):
                similarity_score += 2
            else:
                continue
            # compare dating radius (strict)
            if user_location and profile.location:
                distance = calculate_distance(user_location.lat, user_location.lng, profile.location.lat, profile.location.lng)
                if distance <= user_preference.dating_radius:
                    similarity_score += 2
                else:
                    continue    
            # compare dating reason
            if user_preference.here_for and profile.preference.here_for and user_preference.here_for == profile.preference.here_for:
                similarity_score += 2
            # compare tags
            profile_tags = profile.tags.all()
            common_tags = user_tags.intersection(profile_tags)
            similarity_score += len(common_tags)

            # Compare answers to questions
            profile_questions = profile.question
            if user_questions and profile_questions:
                if user_questions.fav_song == profile_questions.fav_song:
                    similarity_score += 1
                if user_questions.zodiac_sign == profile_questions.zodiac_sign:
                    similarity_score += 1
                if user_questions.drinking == profile_questions.drinking:
                    similarity_score += 1
                if user_questions.smoking == profile_questions.smoking:
                    similarity_score += 1
                if user_questions.religion == profile_questions.religion:
                    similarity_score += 2
                if user_questions.languages == profile_questions.languages:
                    similarity_score += 1
                try:
                    if user_questions.height - 5 <= profile_questions.height <= user_questions.height + 5 :
                        similarity_score += 1
                except:
                    pass    
                try:

                    if user_questions.body_type == profile_questions.body_type:
                        similarity_score += 1
                except:
                    pass        

            if profile.pk in right_swipes:
                similarity_score += 5

            if similarity_score >= SIMILARITY_THRESHOLD:
                potential_matches[profile] += similarity_score
        # sort potential matches by similarity score
        potential_matches = sorted(potential_matches.items(), key=lambda x: x[1], reverse=True)
        # get recommended profiles
        recommended_profiles = [profile for profile, _ in potential_matches[:MAX_RECOMMENDATIONS]]
        serializer = self.get_serializer(recommended_profiles, many=True)
        return Response(serializer.data, status=200)