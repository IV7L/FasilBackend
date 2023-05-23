from rest_framework import viewsets
from rest_framework import permissions
from debate_app.validation.serializers import (
    ContractProposalSerializer,
    VoteProposalSerializer,
    DebateArgSerializer
)
from debate_app.validation.models import (
    ContractProposal,
    VoteProposal,
    DebateArg,
    DAOArgs
)
from debate_app.validation.models import (
    ResourceExternalLink,
    ResourceInternalDebates,
    ResourceUploadFile
)
from debate_app.validation.serializers import (
    ResourceExternalLinkSerializer,
    ResourceInternalDebatesSerializer,
    ResourceUploadFileSerializer,
    DAOArgsSerializer
)

from debate_app.models import Debate, DebateGoal

from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter

class ContractProposalViewSet(viewsets.ModelViewSet):
    queryset = ContractProposal.objects.all().order_by('-date')
    serializer_class = ContractProposalSerializer
    filter_backends = (SearchFilter, )
    search_fields = ['debate__title', ]

class VoteProposalViewSet(viewsets.ModelViewSet):
    queryset = VoteProposal.objects.all().order_by('-date')
    serializer_class = VoteProposalSerializer
    filter_backends = (SearchFilter, )
    search_fields = ['debate__title', ]

class DebateArgViewSet(viewsets.ModelViewSet):
    queryset = DebateArg.objects.all()
    serializer_class = DebateArgSerializer
    filter_backends = (SearchFilter, )
    search_fields = ['debate__title', ]

    def create(self, request, *args, **kwargs):
        debate = request.data['debate']
        goal = request.data['goal']
        debate_object = Debate.objects.get(id = debate)
        goal_object = DebateGoal.objects.get(id = goal)
        if debate_object and goal_object:
            try:
                debate_arg_object = DebateArg.objects.get(Q(debate = debate_object) & Q(goal = goal_object))
            except DebateArg.MultipleObjectsReturned:
                debate_arg_object = DebateArg.objects.filter(Q(debate = debate_object) & Q(goal = goal_object))[0]
            except DebateArg.DoesNotExist:
                debate_arg_object = DebateArg.objects.create(
                    debate = debate_object,
                    goal = goal_object,
                    support_quote = request.data['support_quote'],
                    opposing_quote = request.data['opposing_quote'],
                    rebuttal_conflict1 = request.data['rebuttal_conflict1'],
                    rebuttal_conflict2 = request.data['rebuttal_conflict2'],
                    rebuttal_conflict3 = request.data['rebuttal_conflict3'],
                    rebuttal_question1 = request.data['rebuttal_question1'],
                    rebuttal_question2 = request.data['rebuttal_question2'],
                    rebuttal_question3 = request.data['rebuttal_question3'],
                    rebuttal_conflict_description1 = request.data['rebuttal_conflict_description1'],
                    rebuttal_conflict_description2 = request.data['rebuttal_conflict_description2'],
                    rebuttal_conflict_description3 = request.data['rebuttal_conflict_description3'],
                    rebuttal_question_answer1 = request.data['rebuttal_question_answer1'],
                    rebuttal_question_answer2 = request.data['rebuttal_question_answer2'],
                    rebuttal_question_answer3 = request.data['rebuttal_question_answer3'],
                )
                debate_arg_object.save()
            data = self.get_serializer(debate_arg_object).data

        return Response(data, status=status.HTTP_201_CREATED)

class ResourceExternalLinkViewSet(viewsets.ModelViewSet):
    queryset = ResourceExternalLink.objects.all()
    serializer_class = ResourceExternalLinkSerializer

class ResourceInternalDebatesViewSet(viewsets.ModelViewSet):
    queryset = ResourceInternalDebates.objects.all()
    serializer_class = ResourceInternalDebatesSerializer

class ResourceUploadFileViewSet(viewsets.ModelViewSet):
    queryset = ResourceUploadFile.objects.all()
    serializer_class = ResourceUploadFileSerializer

class DAOArgsViewSet(viewsets.ModelViewSet):
    queryset = DAOArgs.objects.all()
    serializer_class = DAOArgsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['debate__title', ]
