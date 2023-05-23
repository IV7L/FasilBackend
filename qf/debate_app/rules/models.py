from django.db import models
from debate_app.validation.models import (
    ResourceInternalDebates,
    ResourceExternalLink,
    ResourceUploadFile
)
from django.core.validators import MaxValueValidator, MinValueValidator
from AI.main_toxic import *
from django.core.exceptions import ValidationError

# Create your models here.
DEBATE_RULE_STATUS = (
    ('1','Accepted'),
    ('2','Rejected'),
    ('3','Waiting'),
)

class CloseDebateRules(models.Model):
    validation_resource1 = models.ManyToManyField(to=ResourceInternalDebates, blank=True)
    validation_resource2 = models.ManyToManyField(to=ResourceExternalLink, blank=True)
    validation_resource3 = models.ManyToManyField(to=ResourceUploadFile, blank=True)
    user_validation_request_count_on_quote = models.IntegerField(default=1)
    validated_qoals_to_close_count = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self) -> str:
        return super().__str__()
    
    def clean(self) -> None:
        if self.validation_resource1 > 3:
            raise ValidationError('You cant assign more than 3 validation resources of type 1')
        if self.validation_resource2 > 3:
            raise ValidationError('You cant assign more than 3 validation resources of type 1')
        if self.validation_resource3 > 3:
            raise ValidationError('You cant assign more than 3 validation resources of type 1')
        if self.user_validation_request_count_on_quote > 3:
            raise ValidationError('You cant assign more than 3 validation request on quote')
        return super().clean()

class DebateRules(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    user_nft_count = models.IntegerField(default=1) #Form validation: range(3-5) setting from user
    close_debate_rules = models.ForeignKey(CloseDebateRules, on_delete=models.CASCADE)
    status = models.CharField(choices=DEBATE_RULE_STATUS, max_length=255, default='3')# Process Validation to change status from 3:Waiting to 1:Accepted or 2:Rejected

    def __str__(self) -> str:
        return super().__str__()
    
    def clean(self) -> None:
        toxic_score_on_title = test_nlp(self.title)
        toxic_score_on_description = test_nlp(self.desciption)
        if toxic_score_on_title >= 0.5:
            self.status += 1
        else:
            raise ValidationError('Your debate rule title didnt succeded in passing toxic validation')
        if toxic_score_on_description >= 0.5:
            self.status += 1
        else:
            raise ValidationError('Your debate rule description didnt succeded in passing toxic validation')
        return super().clean()