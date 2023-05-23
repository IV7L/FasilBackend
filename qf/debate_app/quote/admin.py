from django.contrib import admin
from debate_app.quote.models import (
    QuoteBoxCategory,
    RecessRoomQuote,
    DebateQuote,
    RecessRoom
)
# Register your models here.
admin.site.register(QuoteBoxCategory)
admin.site.register(RecessRoomQuote)
admin.site.register(DebateQuote)
admin.site.register(RecessRoom)
