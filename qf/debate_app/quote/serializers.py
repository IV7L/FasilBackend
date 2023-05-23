from rest_framework import serializers

from debate_app.quote.models import (
    RecessRoomQuote,
    DebateQuote,
    QuoteBoxCategory,
    RecessRoom
)
from account.serializers import AccountSerializer
from account.models import Account

class RecessRoomQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecessRoomQuote
        fields = ('body', 'father', )
        depth = 4

class DebateQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateQuote
        fields = '__all__'
        depth = 4

class QuoteBoxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteBoxCategory
        fields = '__all__'

class RecessRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecessRoom
        fields = '__all__'
        depth = 4