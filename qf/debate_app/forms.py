from django.forms import ModelForm
from debate_app.models import (
    Debate,
    DebateGoal,
    RecessRoom
)
from debate_app.rules.models import (
    DebateRules,
    CloseDebateRules
)
from debate_app.validation.models import (
    ResourceExternalLink, 
    ResourceInternalDebates,
    ResourceUploadFile
)

class CreateDebateForm(ModelForm):
    class Meta:
        model = Debate
        fields = ['title', 'desciption', ]

class CreateGoalForm(ModelForm):
    class Meta:
        model = DebateGoal,
        fields = ['body', ]

class CreateDebateRuleForm(ModelForm):
    class Meta:
        model = DebateRules
        fields = ['title', 'description', 'user_nft_count', ]

class CreateDebateCloseForm(ModelForm):
    class Meta:
        Model = CloseDebateRules
        fields = ['user_validation_request_count_on_quote', 'validated_qoals_to_close_count', ]

class CreateDebateResourceDebateForm(ModelForm):
    class Meta:
        Model = ResourceInternalDebates
        fields = ['debate', ]

class CreateDebateResourceLinkForm(ModelForm):
    class Meta:
        Model = ResourceExternalLink
        fields = ['link', ]

class CreateDebateResourceFileForm(ModelForm):
    class Meta:
        Model = ResourceUploadFile
        fields = ['file', ]