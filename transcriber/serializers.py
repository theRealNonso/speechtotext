from rest_framework import serializers
import transcriber.models as tm


###############################################################################
# User management and registration
###############################################################################


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = tm.Client
        fields = (
            'username',
            'email',
            'password',
        )

    def create(self, validated_data):
        client = tm.Client.objects.create_user(**validated_data)
        return client


class TranscriptSerializer(serializers.ModelSerializer):

    class Meta:
        model = tm.Transcript
        fields = '__all__'
