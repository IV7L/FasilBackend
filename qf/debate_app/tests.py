from django.test import TestCase

from account.models import (
    Account,
    Team
)
from debate_app.models import (
    Debate,
    DebateCategory,
    DebateGoal,
    DebateRequest,
    DebateRules,
    DebateTimeline,
)
from debate_app.rules.models import (
    QuoteBoxRules,
    DebateRules,
    CloseDebateRules
)
from debate_app.validation.models import (
    ResourceExternalLink,
)


# Create your tests here.
class DebateCreateTestCase(TestCase):
    def setUp(self) -> None:
        main = Account.objects.create(user_hash="main")
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

        team1 = Team.objects.create(
            type='2',
            status='1'
        )

        team2 = Team.objects.create(
            type='2',
            status='1'
        )

        team1.member.set(member_list)
        team2.member.set(member_list)

        # create Debate Goal
        goal0 = DebateGoal.objects.create(
            body='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.''',
            status='1'
        )
        goal1 = DebateGoal.objects.create(
            body='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.''',
            status='1'
        )
        goal2 = DebateGoal.objects.create(
            body='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.''',
            status='3'
        )
        goal3 = DebateGoal.objects.create(
            body='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.''',
            status='3'
        )
        goal4 = DebateGoal.objects.create(
            body='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.''',
            status='3'
        )

        # create Rule Object
        quoteboxrule = QuoteBoxRules.objects.create(
            word_count=50,
            related_to_topic_check_percent=80
        )

        val1req1 = ResourceExternalLink.objects.create(
            link='https:www.8paws.net',
            resource_request_status='1'
        )
        val1req2 = ResourceExternalLink.objects.create(
            link='https:www.9paws.net',
            resource_request_status='1'
        )
        val1req3 = ResourceExternalLink.objects.create(
            link='https:www.10paws.net',
            resource_request_status='1'
        )

        closedebaterules = CloseDebateRules.objects.create(
            user_validation_request_count_on_quote=20,
            validated_qoals_to_close_count=40
        )
        
        closedebaterules.validation_resource2.add(val1req1)
        closedebaterules.validation_resource2.add(val1req2)
        closedebaterules.validation_resource2.add(val1req3)

        rule = DebateRules.objects.create(
            title='main debate rule title',
            description='This is the main debate rule description',
            quote_rules=quoteboxrule,
            user_nft_count=2,
            close_debate_rules=closedebaterules,
        )

        # create debate category
        categ = DebateCategory.objects.create(
            title='Main Category for debate',
        )

        # create debate time line
        tline = DebateTimeline.objects.create()

        debate = Debate.objects.create(
            title='main debate',
            desciption='this is the main debate description',
            creator=main,
            team_1=team1,
            team_2=team2,
            rules=rule,
            category=categ,
            timeline=tline,
            generated_token_request=500,
        )

        debate.goals.add(goal0)
        debate.goals.add(goal1)
        debate.goals.add(goal2)
        debate.goals.add(goal3)
        debate.goals.add(goal4)

        return super().setUp()

    def test_debate_has_done(self):
        team = Debate.objects.get(title='main debate')
        print(team)
