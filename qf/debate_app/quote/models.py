from django.db import models
from account.models import Account, DebateMember, Team
from datetime import timedelta
from django.core.exceptions import ValidationError

from django.core.validators import MaxLengthValidator, MinLengthValidator

from AI.main_toxic import *
from AI.main_related import *
from AI.main_positive import *

from debate_app.models import Debate, DebateGoal


RECESSROOMTYPE = (
    ('1', 'Start Recess'),
    ('2', 'Middle Recess'),
)
DEBATE_QUOTE_CHOICES = (
    ('1','Supporting Quote'),
    ('2','Opposing Quote'),
    ('3','Rebuttal Conflict Quote'),
    ('4','Rebuttal Conflict Description Quote'),
    ('5','Rebuttal Question Quote'),
    ('6','Rebuttal Question Answer Quote'),
)

class QuoteBoxCategory(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        toxic_score_on_title = test_nlp(self.title)
        if toxic_score_on_title >= 0.5:
            pass
        elif toxic_score_on_title >= 0.5:
            raise ValidationError('Your score on Quote Box Category title validation didnt pass')
        return super().clean()

class RecessRoomQuote(models.Model):
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    father = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    goal = models.ForeignKey(to="debate_app.DebateGoal", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()
    
class DebateQuote(models.Model):
    body = models.TextField(validators=[MaxLengthValidator(500), MinLengthValidator(50)])
    father = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    validated = models.BooleanField(default=False)
    NFTed = models.BooleanField(default=False)
    debate = models.ForeignKey(to='debate_app.Debate', on_delete=models.CASCADE)
    goal = models.ForeignKey(to="debate_app.DebateGoal", on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=DEBATE_QUOTE_CHOICES)
    num = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'({self.debate.title}) quotes with type: ({self.get_type_display()}) number: ({self.num})'
    
    def clean(self) -> None:
        similar_results = []

        toxic_passed = False
        positive_passed = False
        related_passed = False

        deb_goals_list = []
        deb = self.debate
        for goal in deb.goals.all():
            deb_goals_list.append(goal.body)

        toxic_score_on_body = test_nlp(self.body)
        positive_score_on_body = test_nlp_positive(self.body)
        similar_results.append(test_similar(self.body, [deb_goals_list[0], deb_goals_list[1], deb_goals_list[2]]))

        if toxic_score_on_body >= 0.5:
            toxic_passed = True
        else:
            toxic_passed = False

        if (positive_score_on_body[1] == 'positive' and positive_score_on_body[0] >= 0):
            positive_passed = True
        else:
            positive_passed = False
        
        if sum(similar_results) / len(similar_results) >= 0: #done
            related_passed = True
        else:
            related_passed = False

        if toxic_passed and positive_passed and related_passed:
            self.validated = True
        else:
            raise ValidationError('Your quote doesnt meet the requirements')

        return super().clean()

class RecessRoom(models.Model):
    type = models.CharField(max_length=255, choices=RECESSROOMTYPE)
    quote = models.ManyToManyField(RecessRoomQuote)
    members = models.ManyToManyField(DebateMember)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    debate = models.ForeignKey(Debate, on_delete=models.SET_NULL, null=True, blank=True)
    goal = models.ForeignKey(DebateGoal, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return 'recess room type: ' + self.get_type_display() + ', for debate: ' + self.debate.title + ', team side: ' + self.team.get_type_display()
