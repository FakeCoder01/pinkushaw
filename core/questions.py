from rest_framework.response import Response
from rest_framework import viewsets
from .models import Question
from .serializers import QuestionSerializer


from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return self.request.user.userprofile.question

    def perform_create(self, serializer):
        serializer.save()

    def question_details(self, request, id=None):
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
        question = self.request.user.userprofile.question
        serializer = self.get_serializer(question, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        

    def destroy(self, request, id=None):
        question = self.request.user.userprofile.question
        question.delete()
        return Response(status=204)
