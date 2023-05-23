from django.contrib import admin
from debate_app.rules.models import (
    CloseDebateRules,
    DebateRules
)
# Register your models here.
admin.site.register(CloseDebateRules)
admin.site.register(DebateRules)