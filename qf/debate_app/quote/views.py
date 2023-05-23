from rest_framework import viewsets, permissions

from debate_app.quote.models import (
    RecessRoomQuote,
    DebateQuote,
    QuoteBoxCategory,
    RecessRoom
)
from debate_app.quote.serializers import (
    RecessRoomQuoteSerializer,
    DebateQuoteSerializer,
    QuoteBoxCategorySerializer,
    RecessRoomSerializer
)

from account.models import Account
from rest_framework.response import Response
from rest_framework import status
from debate_app.models import Debate, DebateGoal
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class RecessRoomQuoteViewSet(viewsets.ModelViewSet):
    queryset = RecessRoomQuote.objects.all()
    serializer_class = RecessRoomQuoteSerializer
    

    def create(self, request, *args, **kwargs):
        current_recess = request.data['recess']
        current_goal = request.data['goal']
        data = {
            'body': request.data['body']
        }
        try:
            father_id = request.data['father']
            father_acc = Account.objects.get(id=father_id)
            data.update({'father': father_acc})
            quote = RecessRoomQuote.objects.create(
                body = data['body'],
                father = father_acc,
                goal = DebateGoal.objects.get(id = current_goal)
            )
            rec = RecessRoom.objects.get(id = current_recess)
            rec.quote.add(quote)
            rec.save()
        except:
            quote = RecessRoomQuote.objects.create(
                body = data['body'],
                father = father_acc,
                goal = DebateGoal.objects.get(id = current_goal)
            )
            rec = RecessRoom.objects.get(id = current_recess)
            rec.quote.add(quote)
            rec.save()
        
        return Response(self.get_serializer(quote).data, status=status.HTTP_201_CREATED)
    

from rest_framework.filters import SearchFilter


class DebateQuoteViewSet(viewsets.ModelViewSet):
    queryset = DebateQuote.objects.all()
    serializer_class = DebateQuoteSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['debate__title', 'validated']

    def create(self, request, *args, **kwargs):
        data = {
            'body': request.data['body'],
        }

        try:
            father_id = request.data['father']
            father_acc = Account.objects.get(id=father_id)
            debate_id = request.data['debate']
            debate_obj = Debate.objects.get(id=debate_id)
            data.update({'father': father_acc})
            data.update({'debate': debate_obj})
            quote = DebateQuote.objects.create(
                body = data['body'],
                father = father_acc,
                debate = debate_obj,
                type = int(request.data['type']),
                num = int(request.data['num'])
            )
            quote.save()
        except:
            pass

        return Response(self.get_serializer(quote).data, status=status.HTTP_201_CREATED)  

    def list(self, request, *args, **kwargs):
        queryset = DebateQuote.objects.all()
        data = self.get_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)

class QuoteBoxCategoryViewSet(viewsets.ModelViewSet):
    queryset = QuoteBoxCategory.objects.all()
    serializer_class = QuoteBoxCategorySerializer

class RecessRoomViewSet(viewsets.ModelViewSet):
    queryset = RecessRoom.objects.all()
    serializer_class = RecessRoomSerializer
    search_fields = ['debate__title', ]
