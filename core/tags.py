from rest_framework.response import Response
from rest_framework import viewsets
from .models import Tag
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class TagManageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def create(self, request):
        if request.data.get('id') != '' and Tag.objects.filter(id=str(request.data.get('id'))).exists():
            tag = Tag.objects.get(id=str(request.data.get('id')))
            profile = self.request.user.userprofile
            profile.tags.add(tag)
            return Response({"details" : "tag added"}, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=413)
    
        
    def destroy(self, request):
        if request.data.get('id') != '' and Tag.objects.filter(id=str(request.data.get('id'))).exists():
            tag = Tag.objects.get(id=str(request.data.get('id')))
            profile = self.request.user.userprofile
            profile.tags.remove(tag)
            return Response({"detail" : "tag deleted"}, status=200)
        return Response({"detail" : "All fields are neccessary"}, status=413)
