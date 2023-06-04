from rest_framework.response import Response
from rest_framework import viewsets
from .models import Preference
from .serializers import PreferenceSerializer


from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.


class PreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = PreferenceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return self.request.user.userprofile.preference

    def perform_create(self, serializer):
        serializer.save()

    def preference_details(self, request, id=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=413)
    

    def update(self, request, id=None):
        preference = self.request.user.userprofile.preference
        serializer = self.get_serializer(preference, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def destroy(self, request, id=None):
        preference = self.request.user.userprofile.preference
        preference.delete()
        return Response(status=204)
