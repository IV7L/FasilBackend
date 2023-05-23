from django.forms import ValidationError
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Account

from debate_app.rules.models import (
    DebateRules,
    CloseDebateRules
)

from debate_app.serializers import (
    DebateSerializer,
    DebateGoalSerializer,
    DebateCategorySerializer,
    DebateTimelineSerializer,
    DebateCreateSerializer
)

from debate_app.models import (
    DebateGoal,
    DebateTimeline,
    DebateCategory,
    Debate,
)

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.forms.models import model_to_dict
from datetime import datetime, timedelta
import pytz
utc=pytz.UTC
from django.utils import timezone
from django.db import transaction

from django.utils.dateparse import parse_datetime
from rest_framework.filters import SearchFilter

# Create your views here.

class DebateCreate(APIView):
    def post(self, request, format=None):
        serializer = DebateCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        snippets = Debate.objects.all()
        serializer = DebateCreateSerializer(snippets, many=True)
        return Response(serializer.data)

class DebateViewSet(viewsets.ModelViewSet):
    queryset = Debate.objects.all()
    serializer_class = DebateSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = Debate.objects.all()
        debate = get_object_or_404(queryset, slug=slug)
        serializer = DebateSerializer(debate, partial=True)
        current_dateTime = timezone.now()

        timeline = debate.timeline
        sub_step_list = [
            debate.timeline.recess_room1,
            debate.timeline.debate_quote1,
            debate.timeline.debate_quote2,
            debate.timeline.recess_room2,
            debate.timeline.rebuttal_conflict,
            debate.timeline.rebuttal_conflict_description,
            debate.timeline.rebuttal_question,
            debate.timeline.rebuttal_question_answer,
            debate.timeline.sub_vote
        ]
        recess_room1 = debate.timeline.start_date + sub_step_list[0]
        debate_quote1 = debate.timeline.start_date + sub_step_list[0] + sub_step_list[1]
        debate_quote2 = debate.timeline.start_date + sub_step_list[0] + sub_step_list[1] + sub_step_list[2]
        recess_room2 = debate.timeline.start_date + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3]
        rebuttal_conflict = debate.timeline.start_date + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4]
        rebuttal_conflict_description = debate.timeline.start_date + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5]
        rebuttal_question = debate.timeline.start_date + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6]
        rebuttal_question_answer = debate.timeline.start_date + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6] + sub_step_list[7]
        sub_vote = debate.timeline.start_date + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6] + sub_step_list[7] + sub_step_list[8]
        
        goal2 = debate.timeline.start_date + debate.timeline.goal1
        goal2_recess_room1 = goal2 + sub_step_list[0]
        goal2_debate_quote1 = goal2 + sub_step_list[0] + sub_step_list[1]
        goal2_debate_quote2 = goal2 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2]
        goal2_recess_room2 = goal2 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3]
        goal2_rebuttal_conflict = goal2 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4]
        goal2_rebuttal_conflict_description = goal2 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5]
        goal2_rebuttal_question = goal2 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6]
        goal2_rebuttal_question_answer = goal2 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6] + sub_step_list[7]
        goal2_sub_vote = goal2 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6] + sub_step_list[7] + sub_step_list[8]
        
        goal3 = debate.timeline.start_date + debate.timeline.goal1 +debate.timeline.goal2
        goal3_recess_room1 = goal3 + sub_step_list[0]
        goal3_debate_quote1 = goal3 + sub_step_list[0] + sub_step_list[1]
        goal3_debate_quote2 = goal3 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2]
        goal3_recess_room2 = goal3 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3]
        goal3_rebuttal_conflict = goal3 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4]
        goal3_rebuttal_conflict_description = goal3 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5]
        goal3_rebuttal_question = goal3 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6]
        goal3_rebuttal_question_answer = goal3 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6] + sub_step_list[7]
        goal3_sub_vote = goal3 + sub_step_list[0] + sub_step_list[1] + sub_step_list[2] + sub_step_list[3] + sub_step_list[4] + sub_step_list[5] + sub_step_list[6] + sub_step_list[7] + sub_step_list[8]

        
        with transaction.atomic():
            if debate.status == '4': #accepted
                if current_dateTime >= debate.timeline.start_date:
                    debate.status = '2'
                    debate.full_clean()
                    debate.save()
                    timeline.super_status = '1'
                    timeline.save()
            
            elif debate.status == '2': #started !! check this:
                if timeline.super_status == '1':
                    if recess_room1 >= current_dateTime > debate.timeline.start_date:
                        timeline.sub_status = '1'
                        timeline.save()
                    if debate_quote1 >= current_dateTime > recess_room1:
                        timeline.sub_status = '2'
                        timeline.save()
                    if debate_quote2 >= current_dateTime > debate_quote1:
                        timeline.sub_status = '3'
                        timeline.save()
                    if recess_room2 >= current_dateTime > debate_quote2:
                        timeline.sub_status = '4'
                        timeline.save()
                    if rebuttal_conflict >= current_dateTime > recess_room2:
                        timeline.sub_status = '5'
                        timeline.save()
                    if rebuttal_conflict_description >= current_dateTime > rebuttal_conflict:
                        timeline.sub_status = '6'
                        timeline.save()
                    if rebuttal_question >= current_dateTime > rebuttal_conflict_description:
                        timeline.sub_status = '7'
                        timeline.save()
                    if rebuttal_question_answer >= current_dateTime > rebuttal_question:
                        timeline.sub_status = '8'
                        timeline.save()
                    if sub_vote >= current_dateTime > rebuttal_question_answer:
                        timeline.sub_status = '9'
                        timeline.save()
                    if current_dateTime > sub_vote:
                        timeline.super_status = '2'
                        timeline.sub_status = '1'
                        timeline.save()
                        #set goal status to completed
                        goal = debate.goals.all()[0]
                        goal.status = '2'
                        goal.save()
                        
                elif timeline.super_status == '2':
                    if goal2_recess_room1 >= current_dateTime > goal2:
                        print(1)
                        timeline.sub_status = '1'
                        timeline.save()
                    if goal2_debate_quote1 >= current_dateTime > goal2_recess_room1:
                        print(2)
                        timeline.sub_status = '2'
                        timeline.save()
                    if goal2_debate_quote2 >= current_dateTime > goal2_debate_quote1:
                        print(3)
                        timeline.sub_status = '3'
                        timeline.save()
                    if goal2_recess_room2 >= current_dateTime > goal2_debate_quote2:
                        print(4)
                        timeline.sub_status = '4'
                        timeline.save()
                    if goal2_rebuttal_conflict >= current_dateTime > goal2_recess_room2:
                        print(5)
                        timeline.sub_status = '5'
                        timeline.save()
                    if goal2_rebuttal_conflict_description >= current_dateTime > goal2_rebuttal_conflict:
                        print(6)
                        timeline.sub_status = '6'
                        timeline.save()
                    if goal2_rebuttal_question >= current_dateTime > goal2_rebuttal_conflict_description:
                        print(7)
                        timeline.sub_status = '7'
                        timeline.save()
                    if goal2_rebuttal_question_answer >= current_dateTime > goal2_rebuttal_question:
                        print(8)
                        timeline.sub_status = '8'
                        timeline.save()
                    if goal2_sub_vote >= current_dateTime > goal2_rebuttal_question_answer:
                        print(9)
                        timeline.sub_status = '9'
                        timeline.save()
                    if current_dateTime >= goal2_sub_vote: #double it !!!
                        timeline.super_status = '3'
                        timeline.sub_status = '1'
                        timeline.save()
                        #set goal status to completed
                        goal = debate.goals.all()[1]
                        goal.status = '2'
                        goal.save()
                        
                elif timeline.super_status == '3':
                    if goal3_recess_room1 >= current_dateTime > goal3:
                        print(1)
                        timeline.sub_status = '1'
                        timeline.save()
                    if goal3_debate_quote1 >= current_dateTime > goal3_recess_room1:
                        print(2)
                        timeline.sub_status = '2'
                        timeline.save()
                    if goal3_debate_quote2 >= current_dateTime > goal3_debate_quote1:
                        print(3)
                        timeline.sub_status = '3'
                        timeline.save()
                    if goal3_recess_room2 >= current_dateTime > goal3_debate_quote2:
                        print(4)
                        timeline.sub_status = '4'
                        timeline.save()
                    if goal3_rebuttal_conflict >= current_dateTime > goal3_recess_room2:
                        print(5)
                        timeline.sub_status = '5'
                        timeline.save()
                    if goal3_rebuttal_conflict_description >= current_dateTime > goal3_rebuttal_conflict:
                        print(6)
                        timeline.sub_status = '6'
                        timeline.save()
                    if goal3_rebuttal_question >= current_dateTime > goal3_rebuttal_conflict_description:
                        print(7)
                        timeline.sub_status = '7'
                        timeline.save()
                    if goal3_rebuttal_question_answer >= current_dateTime > goal3_rebuttal_question:
                        print(8)
                        timeline.sub_status = '8'
                        timeline.save()
                    if goal3_sub_vote >= current_dateTime > goal3_rebuttal_question_answer:
                        print(9)
                        timeline.sub_status = '9'
                        timeline.save()
                    if current_dateTime >= goal3_sub_vote:
                        timeline.super_status = '4'
                        timeline.save()
                        #set goal status to completed
                        goal = debate.goals.all()[2]
                        goal.status = '2'
                        goal.save()
                        
                elif timeline.super_status == '4':
                    pass
                    

            goal1_sub_status = [
                recess_room1,
                debate_quote1,
                debate_quote2,
                recess_room2,
                rebuttal_conflict,
                rebuttal_conflict_description,
                rebuttal_question,
                rebuttal_question_answer,
                sub_vote,
            ]
            goal2_sub_status = [
                goal2_recess_room1,
                goal2_debate_quote1,
                goal2_debate_quote2,
                goal2_recess_room2,
                goal2_rebuttal_conflict,
                goal2_rebuttal_conflict_description,
                goal2_rebuttal_question,
                goal2_rebuttal_question_answer,
                goal2_sub_vote,
            ]
            goal3_sub_status = [
                goal3_recess_room1,
                goal3_debate_quote1,
                goal3_debate_quote2,
                goal3_recess_room2,
                goal3_rebuttal_conflict,
                goal3_rebuttal_conflict_description,
                goal3_rebuttal_question,
                goal3_rebuttal_question_answer,
                goal3_sub_vote,
            ]

            next_value = None
            if timeline.super_status == '1':
                next_value = goal1_sub_status[int(timeline.sub_status) - 1]
            elif timeline.super_status == '2':
                next_value = goal2_sub_status[int(timeline.sub_status) - 1]
            elif timeline.super_status == '3':
                next_value = goal3_sub_status[int(timeline.sub_status) - 1]

            extra_data = {
                'remining_time_for_next': next_value
            }
            data = self.get_serializer(debate).data
            data.update(extra_data)

            return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        validated_data = request.data
        goals = validated_data['goals'] #done
        team_1 = validated_data['team_1'] #done
        team_2 = validated_data['team_2'] #done
        category = validated_data['category']
        rules = validated_data['rules']

        time = DebateTimeline.objects.create(
            start_date = parse_datetime(validated_data['timeline']['start_date']),
            end_date = parse_datetime(validated_data['timeline']['end_date'])
        )

        closerules = CloseDebateRules.objects.create(
            user_validation_request_count_on_quote=rules['close_debate_rules']['user_validation_request_count_on_quote'],
            validated_qoals_to_close_count=rules['close_debate_rules']['validated_qoals_to_close_count']
        )

        rul = DebateRules.objects.create(
            title=rules['title'],
            description=rules['description'],
            user_nft_count=rules['user_nft_count'],
            close_debate_rules=closerules
        )

        debate = Debate.objects.create(
            creator = Account.objects.first(),
            title = validated_data['title'],
            desciption = validated_data['desciption'],
            timeline = time,
            rules = rul,
        )

        for goal in goals:
            go = DebateGoal.objects.create(body=goal['body'])
            debate.goals.add(go)

        for i in category:
            categ = DebateCategory.objects.create(title=i['title'])
            debate.category.add(categ)

        data = self.get_serializer(debate).data

        return Response(data, status=status.HTTP_201_CREATED)

class DebateGoalsViewSet(viewsets.ModelViewSet):
    queryset = DebateGoal.objects.all()
    serializer_class = DebateGoalSerializer

class DebateCategoryViewSet(viewsets.ModelViewSet):
    queryset = DebateCategory.objects.all()
    serializer_class = DebateCategorySerializer

class DebateTimelineViewSet(viewsets.ModelViewSet):
    queryset = DebateTimeline.objects.all()
    serializer_class = DebateTimelineSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()        
        return Response(serializer.data)