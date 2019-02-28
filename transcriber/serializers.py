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
        return (client)


class TranscriptSerializer(serializers.ModelSerializer):
    transcript = serializers.SerializerMethodField('transcribe_file')

    def transcribe_file(self, transcript):
        
        import argparse
        import io
        """Transcribe the given audio file asynchronously."""
        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types
        client = speech.SpeechClient()

        # [START speech_python_migration_async_request]
        with io.open('/home/nonso/Downloads/test1.flac', 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=48000, # 16000
            language_code='en-US')

        # [START speech_python_migration_async_response]
        operation = client.long_running_recognize(config, audio)

        print('Waiting for operation to complete...')
        response = operation.result(timeout=90)

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        x = ''
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            x = x + result.alternatives[0].transcript
        return x
        # [END speech_python_migration_async_response]
    # [END speech_transcribe_async]


    class Meta:
        model = tm.Transcript
        fields = '__all__'


class UriSerializer(serializers.ModelSerializer):

    class Meta:
        model = tm.Transcript
        fields = ('client',)
