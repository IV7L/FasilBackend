from django.shortcuts import render
from account.models import (
    Account,
    Team,
    DebateViewers,
    DebateMember
)
from account.serializers import (
    AccountSerializer,
    RegisterAccountSerializer,
    LoginAccountSerializer,
    SendInvitationSerializer,
    TeamSerializer,
    DebateViewersSerializer,
    DebateMemberSerializer,
    SendInvitationSerializer
)
from rest_framework import viewsets, permissions, generics
from rest_framework import views
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
# Create your views here.

from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
import re

from django.http import JsonResponse
from web3 import Web3
from django.contrib.auth import authenticate, login
import random
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

# eth
from rest_framework.permissions import AllowAny

from debate_app.models import Debate
from debate_app.quote.models import RecessRoom

from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework.filters import SearchFilter


def is_valid_ethereum_address(address):
    if not address:
        return False
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    return True

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'ethereum_address'
    http_method_names = ['get', 'post', 'head', 'put', 'patch']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            full_name = request.data['full_name']
            instance.full_name = full_name
            instance.save()
        except:
            try:
                email = request.data['email']
                instance.email = email
                instance.save()
            except:
                try:
                    phone = request.data['phone_number']
                    instance.phone = phone
                    instance.save()
                except:
                    pass

        instance.save()

        acc = Account.objects.get(id=instance.id)
        acc.is_active = True
        acc.save()

        serializer = self.get_serializer(instance, data=request.data)
        instance.save()
        serializer.is_valid(raise_exception=True)
        
        extra_data = {
            'access_token':str(AccessToken.for_user(acc)),
            'refresh_token':str(RefreshToken.for_user(acc))
        }
        data = serializer.data
        data.update(extra_data)

        
        return Response(data, status=status.HTTP_200_OK)

class RegisterUserAPIView(generics.CreateAPIView):
  serializer_class = RegisterAccountSerializer

class DebateMemberViewSet(viewsets.ModelViewSet):
    queryset = DebateMember.objects.all()
    serializer_class = DebateMemberSerializer
    lookup_field = 'account__ethereum_address'
    http_method_names = ['get', 'post', 'head', 'put', 'patch']

    def create(self, request, *args, **kwargs):
        ethereum_address = request.data['ethereum_address']
        invitation_code = request.data['invitation_code']

        try:
            debate = Debate.objects.get(id = invitation_code[:2])
        except Debate.DoesNotExist:
            debate = None

        try:
            acc = Account.objects.get(ethereum_address = ethereum_address)
            try:
                debate_member = DebateMember.objects.get(account = acc)
            except DebateMember.DoesNotExist:
                debate_member = DebateMember.objects.create(
                    account = acc,
                    debate = debate, 
                    invitation_code = invitation_code, 
                    enrolled = True
                )
            except DebateMember.MultipleObjectsReturned:
                debate_member = DebateMember.objects.filter(account = acc)[0]
        except Account.DoesNotExist:
            acc = Account.objects.create(ethereum_address = ethereum_address)
            try:
                debate_member = DebateMember.objects.get(account = acc)
            except DebateMember.DoesNotExist:
                debate_member = DebateMember.objects.create(
                    account = acc,
                    debate = debate, 
                    invitation_code = invitation_code, 
                    enrolled = True
                )
        
        member_team_type = int(invitation_code[2:4])
        if debate:
            if member_team_type == 0:
                debate_team_1 = debate.team_1
                if debate_team_1:
                    for i in debate_team_1.member.all():
                        if i.id == debate_member.id:
                            pass
                        else:
                            debate_team_1.member.add(debate_member)

                    if not debate.team_1.recess_room1:
                        recess1 = RecessRoom.objects.create(
                            type = '1'
                        )
                        debate.team_1.recess_room1 = recess1
                        debate.team_1.save()
                        debate.team_1.recess_room1.members.add(debate_member)
                        debate.team_1.recess_room1.save()
                    if not debate.team_1.recess_room2:
                        recess2 = RecessRoom.objects.create(
                            type = '2'
                        )
                        debate.team_1.recess_room2 = recess2
                        debate.team_1.save()
                        debate.team_1.recess_room2.members.add(debate_member)
                        debate.team_1.recess_room2.save()
                else:
                    team = Team.objects.create(
                        type = '1'
                    )
                    recess1 = RecessRoom.objects.create(
                        type = '1',
                        debate = debate,
                        team = team
                    )
                    recess2 = RecessRoom.objects.create(
                        type = '2',
                        debate = debate,
                        team = team
                    )
                    team.recess_room1 = recess1
                    team.recess_room2 = recess2
                    team.save()
                    team.member.add(debate_member)
                    debate.team_1 = team
                    debate.save()
            elif member_team_type == 1:
                debate_team_2 = debate.team_2
                if debate_team_2:
                    for i in debate_team_2.member.all():
                        if i.id == debate_member.id:
                            pass
                        else:
                            debate_team_2.member.add(debate_member)
                    if not debate.team_2.recess_room1:
                        recess1 = RecessRoom.objects.create(
                            type = '1'
                        )
                        debate.team_2.recess_room1 = recess1
                        debate.team_2.save()
                        debate.team_2.recess_room1.members.add(debate_member)
                        debate.team_2.recess_room1.save()
                    if not debate.team_2.recess_room2:
                        recess2 = RecessRoom.objects.create(
                            type = '2'
                        )
                        debate.team_2.recess_room2 = recess2
                        debate.team_2.save()
                        debate.team_2.recess_room2.members.add(debate_member)
                        debate.team_2.recess_room2.save()
                else:
                    team = Team.objects.create(
                        type = '2'
                    )
                    recess1 = RecessRoom.objects.create(
                        type = '1',
                        debate = debate,
                        team = team

                    )
                    recess2 = RecessRoom.objects.create(
                        type = '2',
                        debate = debate,
                        team = team
                    )
                    team.recess_room1 = recess1
                    team.recess_room2 = recess2
                    team.save()
                    team.member.add(debate_member)
                    debate.team_2 = team
                    debate.save()


        if debate:
            data = self.get_serializer(debate_member).data
            extra_data = {
                'debate': debate.slug,
                'account_username': debate_member.account.username
            }
            data.update(extra_data)
        else:
            data = self.get_serializer(debate_member).data
        # get team_type => 0 | 1
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = DebateMember.objects.all()
        data = self.get_serializer(queryset, many=True).data
        for item in data:
            acc = Account.objects.get(id=item['account']['id'])
            item['full_name'] = acc.full_name
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.member_order = int(request.data['arrange_value'])
        instance.save()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()        
        return Response(serializer.data)
    
class DebateViewersViewSet(viewsets.ModelViewSet):
    queryset = DebateViewers.objects.all()
    serializer_class = DebateViewersSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['debate__title', ]
    lookup_field = 'account__ethereum_address'

    def create(self, request, *args, **kwargs):
        ethereum_address = request.data['ethereum_address']
        
        if 'vote_code' not in request.data:
            try:
                acc = Account.objects.get(ethereum_address = ethereum_address)
                try: 
                    viewer = DebateViewers.objects.get(account = acc)
                except DebateViewers.DoesNotExist:
                    viewer = DebateViewers.objects.create(
                        account = acc,
                    )
                    viewer.save()
                except DebateViewers.MultipleObjectsReturned:
                    viewer = DebateViewers.objects.filter(account = acc)[0]
                    viewer.save()
            except Account.DoesNotExist:
                acc = Account.objects.create(
                    ethereum_address = ethereum_address
                )
                acc.save()
                try: 
                    viewer = DebateViewers.objects.get(account = acc)
                    viewer.save()
                except DebateViewers.DoesNotExist:
                    viewer = DebateViewers.objects.create(
                        account = acc,
                    )
                    viewer.save()
                except DebateViewers.MultipleObjectsReturned:
                    viewer = DebateViewers.objects.filter(account = acc)[0]
            except Account.MultipleObjectsReturned:
                acc = Account.objects.filter(ethereum_address = ethereum_address)[0]
                try: 
                    viewer = DebateViewers.objects.get(account = acc)
                    viewer.save()
                except DebateViewers.DoesNotExist:
                    viewer = DebateViewers.objects.create(
                        account = acc,
                    )
                    viewer.save()
                except DebateViewers.MultipleObjectsReturned:
                    viewer = DebateViewers.objects.filter(account = acc)[0]
                    viewer.save()

            if viewer.debate:
                data = self.get_serializer(viewer).data
                extra_data = {
                    'debate': viewer.debate.slug
                }
                data.update(extra_data)
            else:
                data = self.get_serializer(viewer).data

            return Response(data, status=status.HTTP_201_CREATED)
            
        else:
            vote_code = request.data['vote_code']

            # vote_code = 123456
            # has_debate: 12
            # has_vote: 34
            # debate: 56

            if vote_code[:2] == '00': has_debate = False
            elif vote_code[:2] == '01': has_debate = True
            if vote_code[2:4] == '00': has_vote = False
            elif vote_code[2:4] == '01': has_vote = True

            try:
                debate = Debate.objects.get(id = int(vote_code[4:]))
            except Debate.DoesNotExist:
                debate = None

            print(has_debate)
            print(has_vote)
            print(debate)

            try:
                acc = Account.objects.get(ethereum_address = ethereum_address)
                try: 
                    viewer = DebateViewers.objects.get(account = acc)
                    viewer.has_vote = has_vote
                    viewer.save()
                    if has_debate:
                        viewer.debate = debate
                        viewer.save()
                except DebateViewers.DoesNotExist:
                    viewer = DebateViewers.objects.create(
                        account = acc,
                        vote_code = vote_code,
                        has_vote = has_vote
                    )
                    if has_debate:
                        viewer.debate = debate
                    viewer.save()
                except DebateViewers.MultipleObjectsReturned:
                    viewer = DebateViewers.objects.filter(account = acc)[0]
                    viewer.has_vote = has_vote
                    viewer.save()
                    if has_debate:
                        viewer.debate = debate
                        viewer.save()
            except Account.DoesNotExist:
                acc = Account.objects.create(
                    ethereum_address = ethereum_address
                )
                acc.save()
                try: 
                    viewer = DebateViewers.objects.get(account = acc)
                    viewer.has_vote = has_vote
                    viewer.save()
                    if has_debate:
                        viewer.debate = debate
                        viewer.save()
                except DebateViewers.DoesNotExist:
                    viewer = DebateViewers.objects.create(
                        account = acc,
                        vote_code = vote_code,
                        has_vote = has_vote
                    )
                    if has_debate:
                        viewer.debate = debate
                    viewer.save()
                except DebateViewers.MultipleObjectsReturned:
                    viewer = DebateViewers.objects.filter(account = acc)[0]
                    viewer.has_vote = has_vote
                    viewer.save()
                    if has_debate:
                        viewer.debate = debate
                        viewer.save()
            except Account.MultipleObjectsReturned:
                acc = Account.objects.filter(ethereum_address = ethereum_address)[0]
                try: 
                    viewer = DebateViewers.objects.get(account = acc)
                    viewer.has_vote = has_vote
                    viewer.save()
                    if has_debate:
                        viewer.debate = debate
                        viewer.save()
                except DebateViewers.DoesNotExist:
                    viewer = DebateViewers.objects.create(
                        account = acc,
                        vote_code = vote_code,
                        has_vote = has_vote
                    )
                    if has_debate:
                        viewer.debate = debate
                    viewer.save()
                except DebateViewers.MultipleObjectsReturned:
                    viewer = DebateViewers.objects.filter(account = acc)[0]
                    viewer.has_vote = has_vote
                    viewer.save()
                    if has_debate:
                        viewer.debate = debate
                        viewer.save()

            if debate:
                data = self.get_serializer(viewer).data
                extra_data = {
                    'debate': debate.slug
                }
                data.update(extra_data)
            else:
                data = self.get_serializer(viewer).data

            return Response(data, status=status.HTTP_201_CREATED)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class BasicAuthAPIView(views.APIView):
    def post(self, request, format=None):
        serializer = LoginAccountSerializer(data=self.request.data, context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return Response({
            'refresh_token':str(refresh_token),
            'access_token': str(access_token)
        }, status=status.HTTP_202_ACCEPTED)
    
class EthereumAuthView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ethereum_address = request.data.get('ethereum_address')
        if ethereum_address:
            try:
                user = Account.objects.get(ethereum_address=ethereum_address)
                serializer = AccountSerializer(user)
                #  check if user related to an active member || active viewer
                # active debate: debate.accepted || debate.started
                # get debate_member 
                try:
                    debate_mem = DebateMember.objects.get(account = user)
                    type = 'debate_member'
                    debate = debate_mem.debate.slug
                except DebateMember.DoesNotExist: 
                    try:
                        debate_viewer = DebateViewers.objects.get(account = user)
                        type = 'debate_viewer'
                        debate = debate_viewer.debate.slug    
                    except DebateViewers.DoesNotExist:
                        type = ''
                        debate = ''

                return Response({
                    'user': {
                        'id': user.id,
                        'ethereum_address': user.ethereum_address,
                        'attached': {
                            'type': type,
                            'debate': debate
                        }
                    },
                    'access_token': str(AccessToken.for_user(user)),
                    'refresh_token': str(RefreshToken.for_user(user))
                }, status=status.HTTP_200_OK)
                return Response(serializer.data)
            except Account.DoesNotExist:
                user = Account.objects.create_user(
                    ethereum_address=ethereum_address,
                    username=ethereum_address,
                    password=None,
                )
                serializer = AccountSerializer(user)
                # Generate an authentication token for the user
                return Response({
                    'user': {
                        'id': user.id,
                        'ethereum_address': user.ethereum_address,
                    },
                    'access_token': str(AccessToken.for_user(user)),
                    'refresh_token': str(RefreshToken.for_user(user))
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Missing Ethereum address'}, status=status.HTTP_400_BAD_REQUEST)
        
class SendInvitationView(views.APIView):
    def post(self, request, format=None):
        serializer = SendInvitationSerializer(data= self.request.data, context = { 'request': self.request })
        serializer.is_valid(raise_exception=True)
        # check and send email | phone number
        phone_regex = r'^\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
        email_regex = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'

        contact = self.request.data['contact']
        debate = Debate.objects.get(title = self.request.data['debate'])
        team_type = self.request.data['team_type']
        inv_type = self.request.data['inv_type']

        if re.match(phone_regex, contact):
            print('valid phone')
            # send invitation link using sms
        elif re.match(email_regex, contact):
            debate_id = str(debate.id).zfill(2)
            if team_type == 'team_1': team_id = '00'
            elif team_type == 'team_2': team_id = '01'
            last_two = str(random.randint(10, 99))
            if inv_type == 'member': inv_type_url = 'invite_code'
            if inv_type == 'viewer': inv_type_url = 'vote_code'
            code_url = debate_id + team_id + last_two
            url = f"http://localhost:3000/?{inv_type_url}={code_url}"            

            subject = 'Invitation link'
            message = f'This is an email contains registering in debate, link: {url}'
            recipient_list = [contact]
            sender = 'pro.iv7l@gmail.com'
            send_mail(subject, message, sender, recipient_list, fail_silently=False)

            # send invitation link using email
        return Response(status = status.HTTP_200_OK)