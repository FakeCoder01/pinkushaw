from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import LeftSwipeSerializer, MatchSerializer, RightSwipeSerializer, TagSerializer
from core.models import Match, LeftSwipe, RightSwipe, Profile, Tag

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_tags(self, request):
        tags = Tag.objects.all()
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data, status=200)


class LeftSwipeViewSet(viewsets.ModelViewSet):

    serializer_class = LeftSwipeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return LeftSwipe.objects.get(user=self.request.user.userprofile)

    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not request.data.get('profile_id') or not Profile.objects.filter(id=request.data.get('profile_id')).exists():
            return Response({'message': 'user not exits'}, status=404)
        left_swiped_user = Profile.objects.get(id=request.data.get('profile_id'))
        if left_swiped_user == self.request.user.userprofile:
            return Response({'message': 'can not left swipe yourself'}, status=404)
        if serializer.is_valid():
            LeftSwipe.objects.get(user=self.request.user.userprofile).disliked_users.add(left_swiped_user)
            return Response(serializer.data, status=200)
        return Response({"detail" : ""}, status=400)
    
    def update(self, request):
        return Response(status=200)
    
    def swipe_details(self, request):
        return Response(status=200)
    
    def destroy(self, request):
        return Response(status=200)
    


class RightSwipeViewSet(viewsets.ModelViewSet):

    serializer_class = RightSwipeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return RightSwipe.objects.get(user=self.request.user.userprofile)
    
    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not request.data.get('whom_liked') or not Profile.objects.filter(id=request.data.get('whom_liked')).exists():
            return Response({'message': 'user not exits'}, status=404)
        right_swiped_user = Profile.objects.get(id=request.data.get('whom_liked'))
        if right_swiped_user== self.request.user.userprofile:
            return Response({'message': 'can not right swipe yourself'}, status=404)
        if RightSwipe.objects.filter(user=self.request.user.userprofile, whom_liked=right_swiped_user).exists():
            return Response({'message' : 'already right swiped'}, status=400)
        
        if serializer.is_valid():

            RightSwipe.objects.create(
                user=self.request.user.userprofile,
                whom_liked = right_swiped_user
            )

            if RightSwipe.objects.filter(user=right_swiped_user, whom_liked=self.request.user.userprofile).exists():
                match = Match.objects.create(
                    first_user = self.request.user.userprofile,
                    second_user = right_swiped_user
                )
                return Response({
                    "message" : "match",
                    "match_id" : match.id,
                    "name" : right_swiped_user.name,
                    "img" : str(right_swiped_user.profile_pic),
                    "age" : right_swiped_user.age,
                    "own_img" : str(self.request.user.userprofile.profile_pic),
                    "city" : right_swiped_user.location.city
                }, status=200)
            
            return Response(serializer.data, status=200)
        return Response({"detail" : ""}, status=400)
    
    def update(self, request):
        return Response(status=200)
    
    def swipe_details(self, request):
        return Response(status=200)
    
    def destroy(self, request):
        return Response(status=200)
        