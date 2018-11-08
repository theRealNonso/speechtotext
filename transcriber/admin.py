from django.contrib import admin

# Register your models here.
import transcriber.models as tm


class TranscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_filter = ['date']
    search_fields = ['email']


class TranscriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'client',
                    'source_file_name',
                    'transcript',
                    'upload_date',
                    )
    list_filter = ['upload_date']
    search_fields = ['client']


admin.site.register(tm.Client, TranscriberAdmin)
admin.site.register(tm.Transcript, TranscriptAdmin)
