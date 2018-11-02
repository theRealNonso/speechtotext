import transcriber.serializers as ts
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import transcriber.models as tm
from django.shortcuts import get_object_or_404
import io
import os
from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


class UploadView(viewsets.ModelViewSet):
    """
    This endpoint uploads files to the
    google cloud storage service using the
    bucket name already created in the model
    and also
    creates an instance in the transcript table
    RW:
        Authenticated users
    """
    queryset = tm.Transcript.objects.all()
    serializer_class = ts.TranscriptSerializer

    def upload_blob(bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))

    def create(self, request):

        def upload_blob(bucket_name, source_file_name, destination_blob_name):
            """Uploads a file to the bucket."""
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_filename(source_file_name)

            print('File {} uploaded to {}.'.format(
                source_file_name,
                destination_blob_name))

        client = tm.Transcript.objects.get(client=request.user)
        source_file_name = request.data['source_file_name']
        destination_blob_name = request.data['destination_blob_name']

        serializer = ts.TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            upload_blob(client.bucket_name, source_file_name, destination_blob_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TranscribeView(viewsets.ModelViewSet):
    """
    This viewsets retrieves all the url of a logged in user
    bearing in mind a user can only have one storage bucket
    """
    queryset = tm.Transcript.objects.all()
    serializer_class = ts.UriSerializer

    @classmethod
    def transcribe_gcs(gcs_uri):
        """Transcribes the audio file specified by the gcs_uri."""

        client = speech.SpeechClient()

        audio = types.RecognitionAudio(uri=gcs_uri)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US')

        response = client.recognize(config, audio)
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            print(u'Transcript: {}'.format(result.alternatives[0].transcript))

    def retrieve(self, request, pk=None):
        queryset = tm.Transcript.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ts.UriSerializer(user)
        return Response(serializer.data)
