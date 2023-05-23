from django.contrib import admin
from account.models import Account, DebateMember, DebateViewers, Team

# Register your models here.
admin.site.register(Account)
admin.site.register(DebateMember)
admin.site.register(DebateViewers)
admin.site.register(Team)