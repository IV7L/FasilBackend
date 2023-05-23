from django.test import TestCase
from account.models import Account, Team

class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(user_hash="main0")
        Account.objects.create(user_hash="main1")
        Account.objects.create(user_hash="main2")
        Account.objects.create(user_hash="main3")
        Account.objects.create(user_hash="main4")

    def test_account_has_hash(self):
        acc = Account.objects.get(user_hash="main0")
        print(acc.user_hash)

class TeamTestCase(TestCase):
    def setUp(self):
        Account.objects.create(user_hash="main0")
        Account.objects.create(user_hash="main1")
        Account.objects.create(user_hash="main2")
        Account.objects.create(user_hash="main3")
        Account.objects.create(user_hash="main4")
        member_list = []
        acc0 = Account.objects.get(user_hash='main0')
        acc1 = Account.objects.get(user_hash='main1')
        acc2 = Account.objects.get(user_hash='main2')
        acc3 = Account.objects.get(user_hash='main3')
        acc4 = Account.objects.get(user_hash='main4')

        member_list.append(acc0)
        member_list.append(acc1)
        member_list.append(acc2)
        member_list.append(acc3)
        member_list.append(acc4)

        team = Team.objects.create(
            status = '2',
            type = '1',
        )
        team.member.set(member_list)

    def test_team_has_members(self):
        team = Team.objects.get(status='2')
        print(team)

