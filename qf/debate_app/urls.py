from django.urls import path, include
from rest_framework import routers
from debate_app.views import index, DebateViewSet

urlpatterns = [
    path('', index, name="index"),
]
