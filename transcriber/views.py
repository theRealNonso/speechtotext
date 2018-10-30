import transcriber.serializers as ts
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
import transcriber.models as tm


class TranscriptView(viewsets.ModelViewSet):
    queryset = tm.Transcript.objects.all()
    serializer_class = ts.TranscriptSerializer
    parser_classes = (MultiPartParser, )

    def perform_create(self, serializer):
        serializer.save(username=self.request.user,
                        file=self.request.data.get('file'),)


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
        return Response(serializer.data)
