from debate_app.validation.models import (
    ContractProposal,
    DAOArgs,
    VoteProposal,
    DebateArg
)
from rest_framework import serializers
from debate_app.validation.models import (
    ResourceExternalLink,
    ResourceInternalDebates,
    ResourceUploadFile
)

class ContractProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractProposal
        fields = '__all__'

class VoteProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteProposal
        fields = '__all__'

class DebateArgSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateArg
        fields = '__all__'

class ResourceExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceExternalLink
        fields = '__all__'

class ResourceInternalDebatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceInternalDebates
        fields = '__all__'

class ResourceUploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceUploadFile
        fields = '__all__'

class DAOArgsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DAOArgs
        fields = '__all__'