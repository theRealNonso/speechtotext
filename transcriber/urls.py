from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
import transcriber.views as tv


router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()
app_router.register(r'upload', tv.TranscriptView, 'upload')
app_router.register(r'gettrint', tv.GetTrintViewset, 'gettrint')

urlpatterns = [
    # documentation
    path('docs/', include_docs_urls(title='Backend API', public=True)),
    path('accounts/', include('rest_registration.api.urls')),
    path('', include(app_router.urls)),
]
