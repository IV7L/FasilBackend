from account.models import (
    Account,
    Team,
    DebateViewers,
    DebateMember
)

from debate_app.models import Debate

from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import authenticate

import string
import random
import math
import re

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    full_name = serializers.CharField(required=False)
    class Meta:
        model = Account
        exclude = ('is_staff', 'last_login', 'is_superuser')
        lookup_field = 'ethereum_address'
  
class DebateMemberSerializer(serializers.ModelSerializer):
    contact = serializers.ReadOnlyField()

    class Meta:
        model = DebateMember
        fields = '__all__'
        depth = 3

class DebateViewersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateViewers
        fields = '__all__'
        depth = 3

class RegisterAccountSerializer(serializers.ModelSerializer):
    public_address = serializers.CharField(max_length=255)
    nonce = serializers.IntegerField(default=math.floor(random.random() * 1000000))
    
    class Meta:
        model = Account
        fields = ('public_address', 'nonce')

    def save(self):
        N = 6
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
        user = Account.objects.create_user(
            username = username,
            public_address = self.validated_data['public_address'],
            password=self.validated_data['public_address'],
            user_auth = True
        )
        user.save()
        return user

class LoginAccountSerializer(serializers.Serializer):
    public_address = serializers.CharField(max_length=255)
    signature = serializers.CharField(max_length = 255)
    nonce = serializers.IntegerField()

    def validate(self, attrs):
        public_address = attrs.get('public_address')
        signature = attrs.get('signature')
        nonce = int(attrs.get('nonce'))

        if public_address and signature:
            user = authenticate(
                public_address=public_address,
                signature=signature,
                nonce=nonce,
            )
            if not user:
                msg = f'No user associated with this public address'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Public Address required...'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs

class TeamSerializer(serializers.ModelSerializer):
    member = DebateMemberSerializer(many=True)
    class Meta:
        model = Team
        fields = '__all__'
        depth = 3

class SendInvitationSerializer(serializers.Serializer):
    contact = serializers.CharField(max_length = 255)
    debate = serializers.CharField(max_length = 255)
    team_type = serializers.CharField(max_length = 255)
    inv_type = serializers.CharField(max_length = 255)

    def validate(self, attrs):
        phone_regex = r'^\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
        email_regex = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'
        contact = attrs.get('contact')
        debate_title = attrs.get('debate')
        team_type = attrs.get('team_type')
        inv_type = attrs.get('inv_type')

        if re.match(phone_regex, contact):
            print('valid phone')
        elif re.match(email_regex, contact):
            print('valid email')
        else:
            msg = 'Not Valid Email ...'
            raise serializers.ValidationError(msg, code='authorization')
        
        try:
            deb = Debate.objects.get(title = debate_title)
        except Debate.DoesNotExist:
            msg = 'Not Valid Debate ...'
            raise serializers.ValidationError(msg, code='authorization')
        
        if team_type != 'team_1' and team_type != 'team_2':
            msg = 'Not Valid team type ... choices are team_1 or team_2'
            raise serializers.ValidationError(msg, code='authorization')
        
        if inv_type != 'member' and inv_type != 'viewer':
            msg = 'Not Valid invitation type ... choices are member or viewer'
            raise serializers.ValidationError(msg, code='authorization')
        
        return super().validate(attrs)
