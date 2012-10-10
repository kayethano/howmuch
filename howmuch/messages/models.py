from django.db import models
from howmuch.core.models import Assignment
from django.contrib.auth.models import User

STATUS_CHOICES = (

	('0', 'CLOSED'),
	('1', 'OPEN'),

	)

class Conversation(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	assignment = models.ForeignKey(Assignment)
	status = models.CharField(max_length=2, default = "1")

	def __unicode__(self):
		return u'Assignment to: %s ' % (self.assignment.requestItem)

class Message(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by Message")
	date = models.DateTimeField(auto_now_add=True)
	message = models.CharField(max_length=250)
	conversation = models.ForeignKey(Conversation)

	def __unicode__(self):
		return u'message: %s' % (self.message)

