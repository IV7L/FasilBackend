from debate_app.rules.models import (
    DebateRules,
    CloseDebateRules
)
from rest_framework import serializers

class CloseDebateRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloseDebateRules
        fields = '__all__'

class DebateRulesSerializer(serializers.ModelSerializer):
    close_debate_rules = CloseDebateRulesSerializer()
    class Meta:
        model = DebateRules
        fields = '__all__'