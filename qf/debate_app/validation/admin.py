from django.contrib import admin
from debate_app.validation.models import (
    ResourceInternalDebates,
    ResourceExternalLink,
    ResourceUploadFile,
    ContractProposal,
    VoteProposal,
    DebateArg,
    DAOArgs
)
# Register your models here.

admin.site.register(ResourceInternalDebates)
admin.site.register(ResourceExternalLink)
admin.site.register(ResourceUploadFile)
admin.site.register(ContractProposal)
admin.site.register(VoteProposal)
admin.site.register(DebateArg)
admin.site.register(DAOArgs)