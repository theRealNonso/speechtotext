from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()

urlpatterns = [
    # documentation
    path('docs/', include_docs_urls(title='Backend API', public=True)),
]
