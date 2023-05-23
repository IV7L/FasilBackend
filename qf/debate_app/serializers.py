from django.shortcuts import get_object_or_404
from debate_app.models import (
    DebateGoal,
    DebateTimeline,
    DebateCategory,
    Debate,
)
from account.models import (
    Team,
    DebateMember,
    Account
)
from debate_app.rules.models import (
    DebateRules,
    CloseDebateRules,
)

from rest_framework import serializers
from account.serializers import TeamSerializer
from debate_app.rules.serializers import DebateRulesSerializer
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import hashlib
from django.core.mail import EmailMessage

from debate_app.quote.models import RecessRoom



def send_invitation_email(email, debate, invite_code):
    event = get_object_or_404(debate, id=event.id)
    subject = 'Invitation to Event: {}'.format(event.title)
    message = 'You have been invited to attend the event {} on {} at {}. Please click on the link below to RSVP: {}'.format(event.title, event.timeline.start_date, 'http://localhost:3000/?invite_code={}'.format(invite_code))
    sender = 'pro.iv7l@gmail.com'
    recipient = email
    send_mail(subject, message, sender, [recipient], fail_silently=False)

def send_vote_email(email, debate, vote_code):
    event = get_object_or_404(debate, id=event.id)
    subject = 'Vote to Event: {}'.format(event.title)
    message = 'You have been invited to attend the event {} on {} at {}. Please click on the link below to RSVP: {}'.format(event.title, event.timeline.start_date, 'http://localhost:3000/?vote_code={}'.format(vote_code))
    sender = 'pro.iv7l@gmail.com'
    recipient = email
    send_mail(subject, message, sender, [recipient], fail_silently=False)

def generate_invite_code(debate, team):
    field1 = str(debate.id).zfill(2)
    field2 = str(team)
    field3 = str(0)
    code = field1 + field2 + field3
    return code

def generate_vote_code(debate, team):
    field1 = str(debate.id).zfill(2)
    field2 = str(team)
    field3 = str(1)
    code = field1 + field2 + field3
    return code

class DebateGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateGoal
        fields = '__all__'

class DebateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateCategory
        fields = '__all__'

class DebateTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateTimeline
        fields = '__all__'

class DebateSerializer(serializers.ModelSerializer):
    goals = DebateGoalSerializer(many=True)
    team_1 = TeamSerializer()
    team_2 = TeamSerializer()
    category = DebateCategorySerializer()
    timeline = DebateTimelineSerializer()
    rules = DebateRulesSerializer()
    category = DebateCategorySerializer(many=True)


    class Meta:
        model = Debate
        fields = '__all__'
        depth = 5
    
    def create(self, validated_data):
        goals = validated_data['goals'] #done
        team_1 = validated_data['team_1'] #done
        team_2 = validated_data['team_2'] #done
        category = validated_data['category']
        rules = validated_data['rules']

        time = DebateTimeline.objects.create(
            start_date = validated_data['timeline']['start_date'],
            end_date = validated_data['timeline']['end_date']
        )
        
        # closerulesval1 = ResourceExternalLink.objects.create(
        #     link = rules['close_debate_rules']['validation_resource1']['link']
        # )
        closerules = CloseDebateRules.objects.create(
            user_validation_request_count_on_quote=rules['close_debate_rules']['user_validation_request_count_on_quote'],
            validated_qoals_to_close_count=rules['close_debate_rules']['validated_qoals_to_close_count']
        )
        # closerules.validation_resource2.add(closerulesval1)

        rul = DebateRules.objects.create(
            title=rules['title'],
            description=rules['description'],
            user_nft_count=rules['user_nft_count'],
            close_debate_rules=closerules
        )
        print(team_1, 'team 1')
        print(team_2, 'team 2')
        for member in team_1['member']:
            regex = r'/^\+?[1-9]\d{1,14}$/' # Regex pattern for phone numbers
            emailRegex = r'/^[^\s@]+@[^\s@]+\.[^\s@]+$/'
                            
            # mem = DebateMember.objects.create(full_name=member['full_name'])
            # te_1.member.add(mem)
            print(member)
            # email = member['contact']
            # print(email)
            pass
            # handle invitation here
            # 1- generate new invitation code using generate_invite_code(debate, account)
            # 2- send an email to memeber using send_invitation_email(request, email, debate, invite_code)
            # http://example.com/?inviteCode=123456

            # email = EmailMessage(
            #     'Subject here', # Subject of the email
            #     'Here is the message.', # Message body
            #     'from@example.com', # "From" address
            #     ['to@example.com'], # List of recipient email addresses
            # )
            # email.send(fail_silently=False)

        for member in team_2['member']:
            # mem = DebateMember.objects.create(full_name=member['full_name'])
            # te_2.member.add(mem)
            pass
            # email = EmailMessage(
            #     'Subject here', # Subject of the email
            #     'Here is the message.', # Message body
            #     'from@example.com', # "From" address
            #     ['to@example.com'], # List of recipient email addresses
            # )
            # email.send(fail_silently=False)

            # handle invitation here
            # 1- generate new invitation code using generate_invite_code(debate, account)
            # 2- send an email to memeber using send_invitation_email(request, email, debate, invite_code)
            # http://example.com/?inviteCode=123456
            
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

        return debate     

class DebateCreateSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    team_1 = serializers.SerializerMethodField()

    class Meta:
        model = Debate
        fields = '__all__'







