from django.contrib import admin
from debate_app.models import (
    Debate,
    DebateCategory,
    DebateGoal,
    DebateRules,
    DebateTimeline,
)
# Register your models here.

admin.site.register(Debate)
admin.site.register(DebateCategory)
admin.site.register(DebateGoal)
admin.site.register(DebateTimeline)
