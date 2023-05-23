from django.forms import ModelForm
from debate_app.validation.models import (
    ResourceInternalDebates,
    ResourceExternalLink,
    ResourceUploadFile
)

class ResourceInternalDebatesForm(ModelForm):
    class Meta:
        model = ResourceInternalDebates
        field = ['debate', ]

class ResourceExternalLinkForm(ModelForm):
    class Meta:
        model = ResourceExternalLink
        field = ['link', ]

class ResourceUploadFileForm(ModelForm):
    class Meta:
        model = ResourceUploadFile
        field = ['file', ]