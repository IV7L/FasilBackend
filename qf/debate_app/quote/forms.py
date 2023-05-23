from django.forms import ModelForm
from debate_app.quote.models import (
    RecessRoomQuote,
    DebateQuote
)

class RecessRoomQuoteForm(ModelForm):
    class Meta:
        model = RecessRoomQuote
        field = ['body', ]

class DebateQuoteForm(ModelForm):
    class Meta:
        model = DebateQuote
        field = ['body', '']