import transcriber.serializers as ts
from rest_framework.response import Response
from rest_framework.views import APIView
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
