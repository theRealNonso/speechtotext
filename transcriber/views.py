import transcriber.serializers as ts
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import transcriber.models as tm
from django.shortcuts import get_object_or_404
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from rest_framework.parsers import MultiPartParser


class TranscriptView(viewsets.ModelViewSet):
    queryset = tm.Transcript.objects.all()
    serializer_class = ts.TranscriptSerializer
    parser_classes = (MultiPartParser, )
    

# class GetTranscriptView(viewsets.ModelViewSet):
#     """
#     This viewsets retrieves all the url of a logged in user
#     bearing in mind a user can only have one storage bucket
#     """
#     queryset = tm.Transcript.objects.all()
#     serializer_class = ts.UriSerializer

#     def retrieve(self, request, pk=None):
#         queryset = tm.Transcript.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = ts.UriSerializer(user)
#         return Response(serializer.data)
