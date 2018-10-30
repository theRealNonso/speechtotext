import transcriber.serializers as ts
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
import transcriber.models as tm
from django.http import HttpResponse


class TranscriptView(viewsets.ModelViewSet):
    queryset = tm.Transcript.objects.all()
    serializer_class = ts.TranscriptSerializer
    parser_classes = (MultiPartParser, )

    def perform_create(self, serializer):
        serializer.save(file=self.request.data.get('file'),)


class GetTrintViewset(viewsets.ViewSet):
    """
    This endpoint is called to display a transcript
    using the trintid
    R:
        Only users authenticated and logged in

    """

    def retrieve(self, request, pk=None):
        queryset = tm.Transcript.objects.all()
        trint = get_object_or_404(queryset, pk=pk)
        serializer = ts.TranscriptSerializer(trint)
        return Response(serializer.data, status=status.HTTP_200_OK)


def uploadtrint(request):
    url = 'https://upload.trint.com/'
    headers = {'api-key': '77f99dcf944ffe0d633d9ca8382c9cd5be53af07'}
    files = {'filename': open('media', 'rb')}
    response = requests.post(url, headers, files=files)
    serializer = ts.TranscriptSerializer(data=response)
    if serializer.is_valid():
        serializer.save()
    return HttpResponse(serializer.data)
