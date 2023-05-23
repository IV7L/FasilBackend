from django.db import models
from account.models import Team, Account
from debate_app.rules.models import DebateRules
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator

from bs4 import BeautifulSoup
from urllib.request import urlopen
from AI.main_toxic import *
from AI.main_related import *
from AI.main_positive import *

from django.db.models.signals import m2m_changed, post_save, pre_save

from debate_app.validation.models import (
    ResourceExternalLink,
    ResourceInternalDebates,
    ResourceUploadFile
)
import uuid
from datetime import timedelta, datetime
from django.dispatch import receiver
from django.core.exceptions import ValidationError

DEBATE_STATUS = (
    ('1', 'Waiting'),
    ('2', 'Started'),
    ('3', 'Rejected'),
    ('4', 'Accepted'),
)
GOAL_STATUS = (
    ('1', 'Not Completed'),
    ('2', 'Completed'),
)
DEBATE_CATEGORY_STATUS = (
    ('1', 'Published'),
    ('2', 'Not Published'),
    ('3', 'Rejected'),
)
DEBATE_SUPER_STATUS = (
    ('0', 'waiting'),
    ('1', 'goal1'),
    ('2', 'goal2'),
    ('3', 'goal3'),
    ('4', 'super_vote'),
)
DEBATE_SUB_STATUS = (
    ('0', 'waiting'),
    ('1', 'recess_room1'),
    ('2', 'debate_quote1'),
    ('3', 'debate_quote2'),
    ('4', 'recess_room2'),
    ('5', 'rebuttal_conflict'),
    ('6', 'rebuttal_conflict_description'),
    ('7', 'rebuttal_question'),
    ('8', 'rebuttal_question_answer'),
    ('9', 'sub_vote'),
)

class DebateGoal(models.Model):
    body = models.TextField(blank=False, validators=[MaxLengthValidator(200)])
    goal_status = models.CharField(choices=GOAL_STATUS, max_length=255, default='0')

    def __str__(self) -> str:
        return self.body
    
    def clean(self) -> None:
        toxic_score = test_nlp(self.body)
        if toxic_score >= 0.5:
            self.status = '1'
        elif toxic_score < 0.5:
            self.status = '2'
        else:
            pass
        return super().clean()
    
class DebateTimeline(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    super_status = models.CharField(choices=DEBATE_SUPER_STATUS, max_length=255, default='0')
    sub_status = models.CharField(choices=DEBATE_SUB_STATUS, max_length=255, default='0')
    
    recess_room1 = models.DurationField(default=timedelta)
    debate_quote1 = models.DurationField(default=timedelta)
    debate_quote2 = models.DurationField(default=timedelta)
    recess_room2 = models.DurationField(default=timedelta)
    rebuttal_conflict = models.DurationField(default=timedelta)
    rebuttal_conflict_description = models.DurationField(default=timedelta)
    rebuttal_question = models.DurationField(default=timedelta)
    rebuttal_question_answer = models.DurationField(default=timedelta)
    sub_vote = models.DurationField(default=timedelta)

    goal1 = models.DurationField(default=timedelta)
    goal2 = models.DurationField(default=timedelta)
    goal3 = models.DurationField(default=timedelta)
    super_vote = models.DurationField(default=timedelta(hours=24))

    def __str__(self) -> str:
        return str(self.start_date)

class DebateCategory(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=DEBATE_CATEGORY_STATUS, default=2)

    def __str__(self) -> str:
        return self.title
    
    def clean(self) -> None:
        toxic_score = test_nlp(self.title)
        if toxic_score >= 0.5:
            self.status = '1'
        elif toxic_score < 0.5:
            self.status = '2'
        else:
            pass
        return super().clean()

class Debate(models.Model):
    title = models.CharField(max_length=255) #done
    desciption = models.TextField(blank=False) #done
    creator = models.ForeignKey(Account, on_delete=models.CASCADE) #done
    team_1 = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='team1', null=True, blank=True, default=None) #done
    team_2 = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='team2', null=True, blank=True, default=None) #done
    goals = models.ManyToManyField(DebateGoal, related_name='debate_goals') #done
    rules = models.ForeignKey(DebateRules, on_delete=models.CASCADE) #done
    category = models.ManyToManyField(DebateCategory) #done
    timeline = models.ForeignKey(DebateTimeline, on_delete=models.CASCADE) #done
    generated_token_request = models.IntegerField(default=0)
    status = models.CharField(choices=DEBATE_STATUS, max_length=255, default='1')
    score = models.IntegerField(default=0)
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)
    

    def __str__(self) -> str:
        return self.title
    
    def clean(self, *args, **kwargs) -> None:
        toxic_score_on_title = test_nlp(self.title)
        toxic_score_on_description = test_nlp(self.desciption)
        if toxic_score_on_title >= 0.5:
            self.score += 1
        if toxic_score_on_description >= 0.5:
            self.score += 1

        # if self.goals.count() > 3:
        #     raise ValidationError('You cant assign more than 3 goals to debate')

        return super(Debate, self).clean(*args, **kwargs)

    
    def save(self, *args, **kwargs) -> None:
        # if self.score >= 10:
        #     self.status = '1'
        # elif 10 > self.score > 5:
        #     self.status = '4'
        # elif 5 > self.score:
        #     self.status = '3'
        return super().save(*args, **kwargs)

def save_profile(sender, instance, **kwargs):
    all_goals = instance.goals.all()
    goals_list = []
    for goal in all_goals:
        if goal.status == '1':
            instance.score += 1
            instance.save()
        goals_list.append(goal)

    if instance.rules.close_debate_rules.validation_resource1.exists():
        next_debates = instance.rules.close_debate_rules.validation_resource1.all()
        similar_results = []
        for resource in next_debates:
            all_debate_goals = resource.debate.goals.all()

            for goal in all_debate_goals:
                similar_results.append(test_similar(goal.body,[goals_list[0].body, goals_list[1].body, goals_list[2].body]))

            internal_debate_object = ResourceInternalDebates.objects.get(id=resource.id)
            if sum(similar_results) / len(similar_results) >= 0:
                internal_debate_object.resource_request_status = '1'
                internal_debate_object.save()
            elif sum(similar_results) / len(similar_results) < 0:
                internal_debate_object.resource_request_status = '2'
                internal_debate_object.save()
            else:
                pass
    if instance.rules.close_debate_rules.validation_resource2.exists():
        all_resources = instance.rules.close_debate_rules.validation_resource2.all()
        similar_results = []
        for resource in all_resources:
            external_link = resource.link
            soup = BeautifulSoup(urlopen(external_link), features="html.parser")
            for data in soup.find_all("p"):
                if len(data.get_text()) >= 10:
                    similar_results.append(test_similar(data.get_text(),[goals_list[0].body, goals_list[1].body, goals_list[2].body]))
                else:
                    pass

            external_link_object = ResourceExternalLink.objects.get(id=resource.id)
            if sum(similar_results) / len(similar_results) >= 0:
                external_link_object.resource_request_status = '1'
                external_link_object.save()
            elif sum(similar_results) / len(similar_results) < 0:
                external_link_object.resource_request_status = '2'
                external_link_object.save()
            else:
                pass
    if instance.rules.close_debate_rules.validation_resource3.exists():
        all_resources = instance.rules.close_debate_rules.validation_resource3.all()
        similar_results = []
        for resource in all_resources:
            with open(resource.file.path, "r") as f:
                for line in f.readlines():
                    if len(line) >= 10:
                        similar_results.append(test_similar(line,[goals_list[0].body, goals_list[1].body, goals_list[2].body]))
                f.close()

            upload_file_object = ResourceUploadFile.objects.get(id=resource.id)
            print(sum(similar_results) / len(similar_results))
            if sum(similar_results) / len(similar_results) >= 0:
                upload_file_object.resource_request_status = '1'
                upload_file_object.save()
            elif sum(similar_results) / len(similar_results) < 0:
                upload_file_object.resource_request_status = '2'
                upload_file_object.save()
            else:
                pass

def save_debate_timeline(sender, instance, *args, **kwargs):
    total_time = instance.end_date - instance.start_date
    super_step_time = total_time / 3
    sub_step_time = super_step_time / 6
    print(super_step_time, sub_step_time, 'are this working ?')
    
    instance.goal1 = super_step_time
    instance.goal2 = super_step_time
    instance.goal3 = super_step_time
    instance.recess_room1 = sub_step_time
    instance.debate_quote1 = sub_step_time / 2
    instance.debate_quote2 = sub_step_time / 2
    instance.recess_room2 = sub_step_time
    instance.rebuttal_conflict = sub_step_time / 4
    instance.rebuttal_conflict_description = sub_step_time / 4
    instance.rebuttal_question = sub_step_time / 4
    instance.rebuttal_question_answer = sub_step_time / 4
    instance.sub_vote = sub_step_time + sub_step_time

def save_debate(sender, instance, *args, **kwargs):
    toxic_score_on_title = test_nlp(instance.title)
    toxic_score_on_description = test_nlp(instance.desciption)
    if toxic_score_on_title >= 0.5:
        instance.score += 1
    if toxic_score_on_description >= 0.5:
        instance.score += 1

    # if instance.goals.count() > 3:
    #     raise ValidationError('You cant assign more than 3 goals to debate')
    
post_save.connect(save_profile, sender=Debate.goals.through)
pre_save.connect(save_debate_timeline, sender=DebateTimeline)
post_save.connect(save_debate, sender=Debate)