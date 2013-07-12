from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Label(models.Model):
	name = models.CharField(max_length=32)
	color = models.CharField(max_length=6)

	def __unicode__(self):
		return self.name


class Issue(models.Model):
	title = models.CharField(max_length=128)
	creator = models.ForeignKey(User, editable=False, related_name='created_issues')
	creation_time = models.DateTimeField(editable=False, default=timezone.now)
	is_open = models.BooleanField(default=True)
	assignee = models.ForeignKey(User, blank=True, null=True, related_name='assigned_issues')
	due_time = models.DateTimeField(blank=True, null=True)
	labels = models.ManyToManyField(Label, related_name='issues')
	# depends_on = models.ManyToManyField('self', symmetrical=False, related_name='required_by')
	content = models.TextField()

	def __unicode__(self):
		return self.title

class IssueHistory(models.Model):
	COMMENT = '.'
	ASSIGN = 'A'
	CHANGE_STATE = 'S'
	SET_DUE = 'D'
	MERGE_TO = 'M'
	MERGE_IN = 'I'
	MODE_CHOICES = (
			(COMMENT, 'Commented'),
			(ASSIGN, 'Assigned to'),
			(CHANGE_STATE, 'Changed state'),
			(SET_DUE, 'Set due time'),
			(MERGE_TO, 'Merged to'),
			(MERGE_IN, 'Merged in')
		)

	issue = models.ForeignKey(Issue, editable=False, related_name='histories')
	user = models.ForeignKey(User, editable=False, related_name='issue_histories')
	timestamp = models.DateTimeField(editable=False, default=timezone.now)
	mode = models.CharField(max_length=1, editable=False, choices=MODE_CHOICES, default=COMMENT)
	content = models.TextField()

	def __unicode__(self):
		return '%s: %s' % (self.mode, unicode(self.timestamp))

