from django.db import models

def upload_loction(instance, filename, **kwars):
    file_path = 'resources/{model}/{filename}'.format(
        model=str(instance._meta.model),
        filename=filename
    )
    return file_path
from django.db.models.signals import m2m_changed, post_save, pre_save

REQUEST_STATUS = (
    ('1','Accepted'),
    ('2','Rejected'),
    ('3','Waiting'),
)
PROPOSAL_STATUS = (
    ('1', 'CREATED'),
    ('2', 'ACTIVE'),
    ('3', 'SUCCEEDED'),
    ('4', 'QUEUED'),
    ('5', 'EXECUTED'),
)

class ResourceInternalDebates(models.Model):
    debate = models.ForeignKey(to='debate_app.Debate', on_delete=models.CASCADE)
    resource_request_status = models.CharField(choices=REQUEST_STATUS, max_length=255, default='3')# Process Validation to change status from 0:Waiting to 1:Accepted or 2:Rejected

    def __str__(self) -> str:
        return self.resource_request_status

class ResourceExternalLink(models.Model):
    link = models.URLField(max_length=200, unique=True)# Form Validation to get the current link data from the site 
    resource_request_status = models.CharField(choices=REQUEST_STATUS, max_length=255)# Process Validation to change status from 0:Waiting to 1:Accepted or 2:Rejected

    def __str__(self) -> str:
        return self.resource_request_status

class ResourceUploadFile(models.Model):
    file = models.FileField(upload_to=upload_loction)
    resource_request_status = models.CharField(choices=REQUEST_STATUS, max_length=255)# Process Validation to change status from 0:Waiting to 1:Accepted or 2:Rejected

    def __str__(self) -> str:
        return self.resource_request_status

class ContractProposal(models.Model):
    debate = models.ForeignKey(to='debate_app.debate', on_delete=models.CASCADE)
    goal = models.ForeignKey(to='debate_app.DebateGoal', on_delete=models.CASCADE)
    network = models.CharField(max_length=255)
    proposal_id = models.CharField(max_length=255)
    proposal_description = models.TextField(blank=True)
    proposal_args = models.TextField(blank=True)
    sender_hash = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    governor = models.CharField(max_length=255)
    box = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    start_block = models.IntegerField(default=0)
    end_block = models.IntegerField(default=0)
    team1_voting_count = models.IntegerField(default=0)
    team2_voting_count = models.IntegerField(default=0)
    voting_status = models.BooleanField(default=True)
    proposal_status = models.CharField(max_length=255, choices=PROPOSAL_STATUS, default='1')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return super().__str__()

class VoteProposal(models.Model):
    debate = models.ForeignKey(to='debate_app.debate', on_delete=models.CASCADE)
    proposal_id = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    signer = models.CharField(max_length=255)
    governor = models.CharField(max_length=255)
    vote_way = models.CharField(max_length=255)
    governor_state_after_vote = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.debate.title + ' vote state'
    
class DebateArg(models.Model):
    debate = models.ForeignKey(to='debate_app.debate', on_delete=models.CASCADE)
    goal = models.ForeignKey(to='debate_app.DebateGoal', on_delete=models.CASCADE)
    support_quote = models.TextField(blank=True)
    opposing_quote = models.TextField(blank=True)
    rebuttal_conflict1 = models.TextField(blank=True)
    rebuttal_conflict2 = models.TextField(blank=True)
    rebuttal_conflict3 = models.TextField(blank=True)
    rebuttal_question1 = models.TextField(blank=True)
    rebuttal_question2 = models.TextField(blank=True)
    rebuttal_question3  = models.TextField(blank=True)
    rebuttal_conflict_description1 = models.TextField(blank=True)
    rebuttal_conflict_description2 = models.TextField(blank=True)
    rebuttal_conflict_description3 = models.TextField(blank=True)
    rebuttal_question_answer1 = models.TextField(blank=True)
    rebuttal_question_answer2 = models.TextField(blank=True)
    rebuttal_question_answer3 = models.TextField(blank=True)

    def __str__(self) -> str:
        return super().__str__()

class DAOArgs(models.Model):
    debate = models.ForeignKey(to = "debate_app.Debate", on_delete=models.CASCADE)
    goal = models.ForeignKey(to="debate_app.DebateGoal", on_delete=models.CASCADE)
    governance_maxSupply = models.IntegerField(default=500)
    governor_quorumPercentage = models.IntegerField(default=51)
    governor_votingDelay = models.IntegerField(default=0)
    governor_votingPeriod = models.IntegerField(default=0) # 500
    governor_proposalThreshold = models.IntegerField(default=0)
    timelock_minDelay = models.IntegerField(default=0)
    box_value = models.CharField(max_length=255)
    box_owner = models.CharField(max_length=255)
    settings_transferAmount = models.IntegerField(default=1) 
    settings_deployer = models.CharField(max_length=255)

    def __str__(self) -> str:
        return super().__str__()

def change_contract_proposal_status(sender, instance, *args, **kwargs):
    current_proposal_status = instance.proposal_status
    if current_proposal_status == '1':
        instance.proposal_status = '2'
        instance.voting_status = True
        instance.save()
    elif current_proposal_status == '3':
        instance.proposal_status = '4'
        instance.voting_status = True
        instance.save()

pre_save.connect(change_contract_proposal_status, sender=ContractProposal)