from rest_framework import viewsets, permissions
from debate_app.rules.models import (
    DebateRules,
    CloseDebateRules
)
from debate_app.rules.serializers import (
    CloseDebateRulesSerializer,
    DebateRulesSerializer,
)

# Create your views here.
class CloseDebateRulesViewSet(viewsets.ModelViewSet):
    queryset = CloseDebateRules.objects.all()
    serializer_class = CloseDebateRulesSerializer
    
class DebateRulesViewSet(viewsets.ModelViewSet):
    queryset = DebateRules.objects.all()
    serializer_class = DebateRulesSerializer
