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

    def perform_create(self, serializer):
        serializer = ts.TranscriptSerializer(data=self.request.data)
        if serializer.is_valid():
            file = self.request.FILES['file'].read()
            client = speech.SpeechClient()
            audio = types.RecognitionAudio(content=file)
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.AMR_WB,
                sample_rate_hertz=16000,
                language_code='en-US')

            response = client.recognize(config, audio)
            serializer.save()
            print('something')
            print(type(response))
            for result in response.results:
                # returns empty response if file is invalid
                # audio must be less than one minuite
                return Response(result.alternatives[0].transcript, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTranscriptView(viewsets.ModelViewSet):
    """
    This viewsets retrieves all the url of a logged in user
    bearing in mind a user can only have one storage bucket
    """
    queryset = tm.Transcript.objects.all()
    serializer_class = ts.UriSerializer

    def retrieve(self, request, pk=None):
        queryset = tm.Transcript.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ts.UriSerializer(user)
        return Response(serializer.data)
