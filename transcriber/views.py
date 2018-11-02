import transcriber.serializers as ts
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import transcriber.models as tm
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
